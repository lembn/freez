import os
import vendor.click as click


@click.command()
@click.argument("source")
@click.argument("dest")
def cli(source: str, dest: str):
    os.symlink(source, dest)

if __name__ == "__main__":
    cli()
