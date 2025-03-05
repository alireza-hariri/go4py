import click
import os
import subprocess
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


@cli.command()
@click.argument("module_name", required=False)
def build(module_name):
    """Build a go module by running make in its directory.

    If module_name is not provided, searches all directories for Makefiles
    and runs make in each directory that has one.
    """
    if module_name:
        # Build a specific module
        module_dir = Path(module_name)
        if not module_dir.exists():
            click.echo(f"Error: Module directory '{module_name}' does not exist.")
            return

        makefile_path = module_dir / "Makefile"
        if not makefile_path.exists():
            click.echo(f"Error: No Makefile found in '{module_name}' directory.")
            return

        click.echo(f"Building module '{module_name}'...")
        subprocess.run(["make", "-C", str(module_dir), "-j2"])

    else:
        # Search all directories for Makefiles and build them
        built_count = 0
        for item in Path(".").iterdir():
            if item.is_dir():
                makefile_path = item / "Makefile"
                if makefile_path.exists():
                    click.echo(f"Building module in '{item}'...")
                    subprocess.run(["make", "-C", str(item), "-j2"])
                    built_count += 1

        if built_count == 0:
            click.echo("No modules with Makefiles found.")
        else:
            click.echo(f"Built {built_count} module(s).")


if __name__ == "__main__":
    cli()
