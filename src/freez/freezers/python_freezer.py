import subprocess
import os
import shutil
from typing import Callable

from . import freezer
from ... import utils


class PythonFreezer(freezer.Freezer):
    def freeze(self, entry: str, output: str):
        venv_name = f"build"
        self._add_cleanup_path(venv_name)

        utils.logging.log("Preparing build location...")
        utils.general.delete(venv_name)

        utils.logging.log("Initialising build environment...")
        subprocess.run(["python", "-m", "venv", venv_name])

        venv_path_prefix: Callable[[str], str] = lambda exe: os.path.join(
            venv_name,
            "bin" if utils.platform.IS_POSIX else "Scripts",
            exe,
        )

        src = utils.general.dirname(entry)
        utils.logging.log(f"Copying source directory: '{src}'")
        venv_src = os.path.join(venv_name, "src")
        shutil.copytree(src, venv_src)
        utils.logging.log(f"Installing PyInstaller...")
        subprocess.run([venv_path_prefix("pip3"), "install", "pyinstaller"])

        reqs = "requirements.txt"
        if os.path.exists(reqs):
            utils.logging.log(f"Installing {entry} dependencies...")
            subprocess.run(
                [venv_path_prefix("pip3"), "install", "-r", "requirements.txt"]
            )
        else:
            utils.logging.log(
                f"Skipping dependency install because {reqs} not found",
                message_type="WARNING",
            )

        utils.logging.log(
            f"Building {entry} executable to '{os.path.join(utils.general.app_path(self.name))}'."
        )
        self._add_cleanup_path(self.name + ".spec")
        subprocess.run(
            [
                venv_path_prefix("pyinstaller"),
                "--onedir",
                "--distpath",
                output,
                "--name",
                self.name,
                os.path.join(venv_src, os.path.basename(entry)),
            ]
        )
        utils.logging.log("Build complete.", color="green")
