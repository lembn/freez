import os
from typing import Type

import click

from ... import utils
from .. import freezers

FREEZERS: dict[str, Type[freezers.Freezer]] = {"py": freezers.PythonFreezer}


def cli(entry: str, name: str) -> None:
    try:
        entry_name, ext = os.path.splitext(os.path.basename(entry))
        freezer = FREEZERS[ext[1:]](name if name else entry_name)

        print()
        click.secho(f"[[ FREEZ ]]", bold=True, fg="blue", blink=True)

        freezer.freeze(os.path.abspath(entry), utils.general.app_path())
        freezer.install()
    except KeyboardInterrupt:
        utils.logging.log("Stopped.", message_type="WARNING")
    finally:
        utils.logging.log("Cleaning up...")
        freezer.cleanup()
        utils.logging.log("Artefacts removed.", color="green")
