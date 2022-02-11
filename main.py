import re
import subprocess
import os
import shutil
import platform
import sys
from typing import Callable
from datetime import datetime
import vendor.click as click

join: Callable[[str, str], str] = lambda x, y: os.path.join(x, y).replace("\\", "/")

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
    if (os.path.exists(path)):
        remove(path)

@click.command()
@click.version_option("1.2.2")
@click.argument("entry", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "-o",
    "--output",
    default="./",
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
    is_flag = True,
    help="Install the executable into the python script path to make it globally accessible across the system (this will ignore the path set by --output).",
)
def cli(entry: str, output: str, name: str, _global: bool) -> None:
    """
    Create single-file executables from python scripts.

    \b
    ENTRY: The entry point script of the program being built.
    """

    remove_pipenv = False

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

    print()
    log("Installing freez dependencies...")
    subprocess.run(["pipenv", "install", "--skip-lock", "pipreqs", "pyinstaller"])

    try:
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
        os.remove(requirements)

        if _global:
            output = join(os.path.dirname(sys.executable), "Scripts")
        elif not os.path.exists(output):
            os.makedirs(output)
        log(f"Building executable to {output}")
        if not name:
            name = re.sub(r"([\.\w]+[\\/])+", "", entry)
            name = re.sub("(\.py)", "", name)
        if platform.system().upper() == "WINDOWS":
            name += ".exe"
        subprocess.run(["pipenv", "run", "pyinstaller", entry, "--onefile", "--name", name])
        shutil.move(f"./dist/{name}", join(output, name))
    except PermissionError as e:
        print()
        log(e, type="ERROR", colour="red")
        log("Global installations require 'sudo' on Unix or 'Run as administrator' on Windows")
    except KeyboardInterrupt:
        print()
        log("Aborted!")
    finally:
        print()
        log("Cleaning up...")
        delete(f"./{name}.spec", False)
        delete("./build")
        delete("./dist")
        pycache = "__pycache__"
        delete(pycache)
        entry_pycache = join(entry_parent, pycache)
        delete(entry_pycache)
        log("Artefacts removed.")
        subprocess.run(["pipenv", "--rm"])
        if remove_pipenv:
            subprocess.run(["pip3", "uninstall", "-y", "pipenv"])


if __name__ == "__main__":
    cli(prog_name="freez")
