import click
from typing import Literal
import datetime as dt

LOG_COLOURS = {"INFO": "white", "WARNING": "bright_yellow", "ERROR": "red"}


def log(
    message: str,
    message_type: Literal["INFO", "WARNING", "ERROR"] = "INFO",
    color: str = None,
) -> None:
    click.secho(
        f"{message_type} [{dt.datetime.now().strftime('%H:%M:%S')}]: {message}",
        bold=True,
        fg=color if color else LOG_COLOURS[message_type],
    )
