import click
import os
import subprocess
from pathlib import Path

from go4py.template_engine import render_template

HERE = Path(__file__).parent
TEMPLATE_DIR = HERE / "templates"


@click.group()
def cli():
    """go4py CLI"""
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

    # Check if we're already inside a Go module (check current and parent directory)
    current_go_mod_exists = Path("go.mod").exists()
    parent_go_mod_exists = Path("..").joinpath("go.mod").exists()

    if not (current_go_mod_exists or parent_go_mod_exists):
        # initialize a go module in root directory
        os.system(f"go mod init {module_name}")
    else:
        click.echo("Already inside a Go module, skipping 'go mod init'")

    # for all files in template folder copy them to the module folder
    data = {"module_name": module_name.split("/")[-1]}
    for file in TEMPLATE_DIR.iterdir():
        dst_file = module_dir / file.relative_to(TEMPLATE_DIR)
        dst_file.write_text(render_template(file.read_text(), data))

    # print a message
    click.echo(f"Module {module_name} initialized.")


@cli.command()
@click.argument("build_path", required=False, default=".")
def build(build_path):
    """Build a go module by running make in its directory.

    If module_name is not provided, searches all directories for Makefiles
    and runs make in each directory that has one.
    """
    build_path = Path(build_path)
    if not build_path.exists():
        click.echo(f"Error: Module directory '{build_path}' does not exist.")
        exit(1)

    makefile_path = build_path / "Makefile"
    if makefile_path.exists():
        click.echo(f"Building module '{build_path}'...")
        subprocess.run(["make", "-C", str(build_path), "-j2"])

    else:
        # Search all directories for Makefiles and build them
        built_count = 0
        for item in build_path.iterdir():
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


@cli.command()
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def parse(args):
    """parse go files in a directory to find exported functions."""
    exetutable = HERE / "parse"
    if not exetutable.exists():
        # try to build it
        os.system(f"go build -o {str(exetutable)} {HERE / '../go_cmd/parse'}")
    if not exetutable.exists():
        click.echo("Error: parse executable not found.")
        # exit with error
        exit(1)
    cmd = [str(exetutable)] + list(args)
    subprocess.run(cmd)


if __name__ == "__main__":
    cli()
