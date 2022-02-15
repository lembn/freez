import ctypes
import re
import subprocess
import os
import shutil
import platform
import sys
from time import sleep
from typing import Callable
from datetime import datetime
import vendor.click as click

join: Callable[[str, str], str] = lambda x, y: os.path.join(x, y).replace("\\", "/")
winpath: Callable[[str], str] = lambda x: '"' + os.path.abspath(x) + '"'


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
@click.version_option("1.4.5")
@click.argument("entry", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "-o",
    "--output",
    default=".",
    show_default=True,
    type=click.Path(exists=True, file_okay=False),
    help="Output folder of the built executable.",
)
@click.option(
    "-n",
    "--name",
    type=click.STRING,
    help="Name of the built executable (defaults to name of entry point script).",
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

        scope = "globally" if _global else "locally"
        log(f"Building executable {scope}.")
        if not name:
            name = re.sub(r"([\.\w]+[\\/])+", "", entry)
            name = re.sub("(\.py)", "", name)
        if platform.system().upper() == "WINDOWS":
            name += ".exe"
        subprocess.run(
            ["pipenv", "run", "pyinstaller", entry, "--onefile", "--name", name]
        )

        # sys.executable will already include "/Scripts" if freez is running from installed executable so we check
        if _global:
            print()
            log("Installing...")
            exe_dir = os.path.dirname(sys.executable)
            if platform.system() == "Windows":
                output = exe_dir if "Scripts" in exe_dir else join(exe_dir, "Scripts")
                exe = join(output, name)
                exists = os.path.exists(exe)
                if exists:
                    ctime = float(os.path.getctime(exe))
                # ShellExecute runs executables and the Windows `move` and `copy` commands aren't actual executables so can't be used
                ctypes.windll.shell32.ShellExecuteW(
                    None,
                    "runas",
                    "robocopy",
                    f'{winpath("./dist")} {winpath(output)} {name}',
                    None,
                    1,
                )
                # wait for robocopy to complete. we can't just check for file existence becuase if the executable is being overwrittern it will already exist
                if exists:
                    wait = lambda: float(os.path.getctime(exe)) == ctime
                else:
                    wait = lambda: not os.path.isfile(exe)
                while wait():
                    sleep(0.2)
            else:
                subprocess.call(
                    [
                        "/usr/bin/sudo",
                        "mv",
                        os.path.abspath(f"./dist/{name}"),
                        os.path.abspath(join(exe_dir, name)),
                    ]
                )
        else:
            if not os.path.exists(output):
                os.makedirs(output)
            shutil.move(f"./dist/{name}", join(output, name))
        log("Installed.")
    except KeyboardInterrupt:
        print()
        log("Aborted!")
    finally:
        print()
        log("Cleaning up...")
        delete(f"./requirements.txt", False)
        delete(f"./{name}.spec", False)
        delete(f"./Pipfile", False)
        delete("./build")
        delete("./dist")
        pycache = "__pycache__"
        delete(pycache)
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
