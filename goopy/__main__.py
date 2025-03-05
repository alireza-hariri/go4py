import IPython
import click
import os
from pathlib import Path

from goopy.template_engine import render_template

HERE = Path(__file__).parent
TEMPLATE_DIR = HERE / "templates"


@click.group()
def cli():
    """A simple CLI with an init command."""
    pass


@cli.command()
@click.argument("module_name")
def init(module_name):
    """Initialize a go module with the given name."""

    module_dir = Path(module_name)
    if module_dir.exists():
        click.echo(f"A directory with the name of {module_name} already exists.")
        return
    # create directory with the name of the module and cd there
    module_dir.mkdir()
    # initialize a go module in root directory
    os.system(f"go mod init {module_name}")
    # for all files in template folder copy them to the module folder
    data = {"module_name": module_name}
    for file in TEMPLATE_DIR.iterdir():
        dst_file = module_dir / file.relative_to(TEMPLATE_DIR)
        dst_file.write_text(render_template(file.read_text(), data))

    # print a message
    click.echo(f"Module {module_name} initialized.")


if __name__ == "__main__":
    cli()
