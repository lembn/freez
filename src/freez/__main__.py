from typing import Optional

import click

from . import commands

# TODO: create uninstall command
# TODO: ^ v.2.2.0


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option("2.1.0")
@click.argument("entry", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "-n",
    "--name",
    type=click.STRING,
    help="Name of the executable bundle (defaults to name of entry point script).",
)
def cli(ctx: click.Context, entry: str, name: Optional[str]) -> None:
    """
    Create executables from interpreted language programs. Intergrated terminals
    in certain programs may have to be restarted for changes to take effect.

    \b
    ENTRY: The entry point script of the program being built.
    """
    if ctx.invoked_subcommand is None:
        commands.cli(entry, name)


if __name__ == "__main__":
    cli(prog_name="freez")
