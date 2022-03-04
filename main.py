import re
import subprocess
import os
import shutil
import platform
from typing import Callable
from datetime import datetime
import winreg
import vendor.click as click

join: Callable[[str, str], str] = lambda x, y: os.path.join(x, y).replace("\\", "/")
join3: Callable[[str, str, str], str] = lambda x, y, z: join(join(x, y), z)
winpath: Callable[[str], str] = lambda x: '"' + x.replace("/", "\\") + '"'

WINDOWS = "Windows"

SRC_KEY = "__SOURCE__"
WIN_UNINSTALLER_SCRIPT = f"""\
import winreg
reg_key = "Environment"
reg_subkey = "Path"
with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, access=winreg.KEY_READ) as reg_handle:
    reg_val, _ = winreg.QueryValueEx(reg_handle, reg_subkey)
    if {SRC_KEY} in reg_val:
        reg_val = reg_val.replace({SRC_KEY};, "")
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, access=winreg.KEY_SET_VALUE) as reg_handle:
            winreg.SetValueEx(reg_handle, reg_subkey, 0, winreg.REG_EXPAND_SZ, reg_val)
"""

UNIX_UNINSTALLER_SCRIPT = f"""\
import os
if os.path.exists({SRC_KEY})
    os.remove({SRC_KEY})
"""

def log(message: str, type: str = "INFO", colour: str = "white") -> None:
    click.echo(
        click.style(
            f"{type} [{datetime.now().strftime('%H:%M:%S')}]: {message}",
            bold=True,
            fg=colour,
        )
    )


def delete(path: str, _dir: bool = True):
    remove = shutil.rmtree if _dir else os.remove
    if os.path.exists(path):
        remove(path)


@click.command()
@click.version_option("1.5.0")
@click.argument("entry", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "-o",
    "--output",
    default=".",
    show_default=True,
    type=click.Path(exists=True, file_okay=False),
    help="Output folder of the executable bundle.",
)
@click.option(
    "-n",
    "--name",
    type=click.STRING,
    help="Name of the executable bundle (defaults to name of entry point script).",
)
@click.option(
    "-g",
    "--global",
    "_global",
    is_flag=True,
    help="Install the executable into the python script path to make it globally accessible across the system (this will ignore the path set by --output).",
)
def cli(entry: str, output: str, name: str, _global: bool) -> None:
    """
    Create single-file executables from python scripts.

    \b
    ENTRY: The entry point script of the program being built.
    """

    remove_pipenv = False
    replace_pipfile = False

    print()
    log("Checking required global dependency tools...")
    try:
        subprocess.run(["pipenv", "--version"])
        log(f"Found pipenv.")
    except FileNotFoundError:
        log(f"Failed to find pipenv.", type="WARN", colour="yellow")
        try:
            log("Checking pip...")
            subprocess.run(["pip3", "--version"])
            log("Found pip.")
            log(f"Installing pipenv (it will be removed later)...")
            subprocess.run(["pip3", "install", "pipenv"])
            remove_pipenv = True
        except FileNotFoundError:
            log("Failed to find pip.", type="ERROR", colour="RED")
            log("Unable to install requried dependencies\nAborting...")
            return

    try:
        print()
        log("Installing freez dependencies...")
        if os.path.exists("./Pipfile"):
            shutil.copy("./Pipfile", "./Pipfile.STORE")
            replace_pipfile = True
        subprocess.run(["pipenv", "install", "--skip-lock", "pipreqs", "pyinstaller"])

        print()
        log(f"Collecting {entry} dependencies...")
        args = ["pipenv", "run", "pipreqs", "--force"]
        entry_parent = os.path.dirname(os.path.abspath(entry))
        args.append(entry_parent)
        subprocess.run(args)

        print()
        log(f"Installing {entry} dependencies...")
        requirements = join(entry_parent, "requirements.txt")
        subprocess.run(["pipenv", "install", "-r", requirements, "--skip-lock"])

        print()
        log("Dependencies installed.")
        delete(requirements, False)

        scope = "global" if _global else "local"
        log(f"Building {scope} executable to '{output}'.")
        if not name:
            name = re.sub(r"([\.\w]+[\\/])+", "", entry)
            name = re.sub("(\.py)", "", name)
        subprocess.run(
            [
                "pipenv",
                "run",
                "pyinstaller",
                "--onedir",
                "--distpath",
                output,
                "--name",
                name,
                entry,
            ]
        )

        if _global:
            print()
            log("Installing...")
            source = os.path.abspath(join(output, name))
            if platform.system() == WINDOWS:
                reg_key = "Environment"
                reg_subkey = "Path"
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, access=winreg.KEY_READ) as reg_handle:
                    reg_val, _ = winreg.QueryValueEx(reg_handle, reg_subkey)
                    if source not in reg_val:
                        reg_val += winpath(source) + ";"
                        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, access=winreg.KEY_SET_VALUE) as reg_handle:
                            winreg.SetValueEx(reg_handle, reg_subkey, 0, winreg.REG_EXPAND_SZ, reg_val)
            else:
                with open(f"etc/profile.d/{name}.sh", "w") as f:
                    f.write(f"$PATH:{source}")
            log("Installed.")
            print()
            log("Creating uninstaller...")
            uninstaller_path = join(output, f"{name}-uninstaller.py")
            with open(f"etc/profile.d/{name}.sh", "w") as f:
                    f.write(WIN_UNINSTALLER_SCRIPT.replace(SRC_KEY, source)
                            if platform.system() == WINDOWS
                            else UNIX_UNINSTALLER_SCRIPT.replace(SRC_KEY, source))
            subprocess.run(
                [
                    "pipenv",
                    "run",
                    "pyinstaller",
                    "--onefile",
                    "--distpath",
                    output,
                    uninstaller_path,
                ]
            )
            log("Uninstaller build successful.")
        else:
            log("Installed.")

    except KeyboardInterrupt:
        print()
        log("Stopped.")
    finally:
        print()
        log("Cleaning up...")
        delete("./requirements.txt", False)
        delete(f"./{name}.spec", False)
        delete("./Pipfile", False)
        delete("./build")
        pycache = "__pycache__"
        delete(pycache)
        if entry_parent:
            entry_pycache = join(entry_parent, pycache)
            delete(entry_pycache)
        if replace_pipfile:
            subprocess.run(["pipenv", "--rm"])
            log("Reconstructing original virtual environment...")
            os.rename("./Pipfile.STORE", "./Pipfile")
            subprocess.run(["pipenv", "install", "-d"])
            log("Environment restored.")
        log("Artefacts removed.")
        if remove_pipenv:
            log("Removing pipenv")
            subprocess.run(["pip3", "uninstall", "-y", "pipenv"])
        log("Build successful.", colour="green")


if __name__ == "__main__":
    cli(prog_name="freez")
