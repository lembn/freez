import os
import subprocess

from .. import utils

# TODO: launcher scripts have changed so check that they still work

if __name__ == "__main__":
    print("Initialising Freez environment")
    subprocess.run(["python", "-m", "venv", "."])
    subprocess.run(
        [
            os.path.join(
                ".",
                "bin" if utils.platform.IS_POSIX else "Scripts",
                "pip3",
            ),
            "install",
            "-r",
            "requirements.txt",
        ]
    )

    launcher_script: str = None
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "launchers",
            os.name + utils.platform.SCRIPT_EXT,
        )
    ) as file:
        launcher_script = file.read()

    launcher_script = launcher_script.replace(
        "INSERT_FREEZ_PATH",
        os.path.abspath("."),
    )

    app_path = utils.general.app_path()
    os.makedirs(app_path, exist_ok=True)
    with open(
        os.path.join(
            app_path,
            "freez" + utils.platform.SCRIPT_EXT,
        ),
        "w",
    ) as file:
        file.write(launcher_script)

    print("\nFreez is initialised.")
    print(
        "To make Freez (and the programs it installs) globally accesible, add the following to your PATH environment variable:"
    )
    print(f"  - {app_path}")
    print()
