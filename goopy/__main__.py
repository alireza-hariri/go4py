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
    # create directory with the name of the module and cd there
    os.system(f"mkdir -p {module_name}")
    os.chdir(module_name)
    # create a go module with the name of the module
    os.system(f"go mod init {module_name}")
    # for all files in template folder copy them to the module folder
    data = {"module_name": module_name}
    for file in TEMPLATE_DIR.iterdir():
        dst_file = file.relative_to(TEMPLATE_DIR)
        dst_file.write_text(render_template(file.read_text(), data))

    # print a message
    click.echo(f"Module {module_name} initialized.")


if __name__ == "__main__":
    cli()
