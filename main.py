import re
import subprocess
import os
import shutil
import platform
from typing import Callable
from datetime import datetime
import vendor.click as click

join: Callable[[str, str], str] = lambda x, y: os.path.join(x, y).replace("\\", "/")

def log(message: str, type: str = "INFO", colour: str = "white") -> None:
    click.echo(
        click.style(
            f"{type} [{datetime.now().strftime('%H:%M:%S')}]: {message}",
            blink=True,
            bold=True,
            fg=colour,
        )
    )

@click.command()
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
def cli(entry: str, output: str, name: str):
    """
    Create single-file executables from python scripts.

    \b
    ENTRY: The entry point script of the program being built.
    """

    remove = False

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
            remove = True
        except FileNotFoundError:
            log("Failed to find pip.", type="ERROR", colour="RED")
            log("Unable to install requried dependencies\nAborting...")
            return

    log("Installing freez dependencies...")
    requirements = join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
    subprocess.run(["pipenv", "install", "-r", requirements, "--skip-lock"])

    shutil.copy("./Pipfile", "./.Pipfile")
    args = ["pipenv", "run", "pipreqs", "--force"]
    entry_parent = os.path.dirname(os.path.abspath(entry))
    args.append(entry_parent)
    log(f"Collecting {entry} dependencies...")
    subprocess.run(args)
    log(f"Installing {entry} dependencies...")
    requirements = join(entry_parent, "requirements.txt")
    subprocess.run(["pipenv", "install", "-r", requirements, "--skip-lock"])
    log("Dependencies installed")
    os.remove(f"./Pipfile")
    os.remove(requirements)
    os.replace("./.Pipfile", "./Pipfile")

    if not name:
        name = re.sub(r"([\.\w]+[\\/])+", "", entry)
        name = re.sub("(\.py)", "", name)
    if platform.system().upper() == "WINDOWS":
        name += ".exe"

    subprocess.run(["pipenv", "run", "pyinstaller", entry, "--onefile", "--name", name])
    os.remove(f"./{name}.spec")
    shutil.rmtree("./build")
    if not os.path.exists(output):
        os.makedirs(output)
    os.replace(f"./dist/{name}", join(output, name))
    shutil.rmtree("./dist")
    pycache = "__pycache__"
    if os.path.exists(pycache):
        shutil.rmtree(pycache)
    entry_pycache = join(entry_parent, pycache)
    if os.path.exists(entry_pycache):
        shutil.rmtree(entry_pycache)

    subprocess.run(["pipenv", "--rm"])

    if remove:
        subprocess.run(["pip3", "uninstall", "pipenv"])


if __name__ == "__main__":
    cli(prog_name="freez")
