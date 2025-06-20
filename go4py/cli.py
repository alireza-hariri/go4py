from importlib import metadata
import sys
import sysconfig
import click
import os
import subprocess
from pathlib import Path

from go4py.template_engine import render_template
from go4py.utils.text_util import print_text_box

HERE = Path(__file__).parent
TEMPLATE_DIR = HERE / "templates"


def find_make_files(build_path):
    build_path = Path(build_path)
    if not build_path.exists():
        click.echo(f"Error: Package directory '{build_path}' does not exist.")
        sys.exit(1)

    makefiles = ("Makefile", "makefile")
    if any((build_path / f).exists() for f in makefiles):
        yield build_path
    else:
        for item in build_path.iterdir():
            if item.is_dir():
                if any((item / f).exists() for f in makefiles):
                    yield item


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
        click.echo("\nAlready inside a Go module, skipping 'go mod init' command")

    # for all files in template folder copy them to the module folder
    data = {"module_name": module_name.split("/")[-1]}
    for file in TEMPLATE_DIR.rglob("*"):
        if file.is_file():
            dst_file = module_dir / file.relative_to(TEMPLATE_DIR)
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            dst_file.write_text(render_template(file.read_text(), data))

    # print a message
    print_text_box(f"Module {module_name} initialized.")


@cli.command()
@click.argument("build_path", required=False, default=".")
def build(build_path):
    """Build a go module by running make in its directory.

    If module_name is not provided, searches all directories for Makefiles
    and runs make in each directory that has one.
    """
    build_path = Path(build_path)
    if not build_path.exists():
        click.echo(f"Error: Package directory '{build_path}' does not exist.")
        exit(1)

    for makepath in find_make_files(build_path):
        click.echo(f"Building module '{makepath}'...")
        subprocess.run(["make", "-C", str(makepath)])


@cli.command()
@click.argument("build_path", required=False, default=".")
def clean(build_path):
    """Clean all build artifacts."""
    for makepath in find_make_files(build_path):
        subprocess.run(["make", "-C", str(makepath), "clean"])


@cli.command()
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def parse(args):
    """parse go files in a directory to find exported functions."""
    exetutable = HERE / "parse"
    if not exetutable.exists():
        # try to build it
        os.system(f"go build -o {str(exetutable)} {HERE / './go_cmd/parse/main.go'}")
    if not exetutable.exists():
        click.echo("Error: parse executable not found.")
        # exit with error
        exit(1)
    cmd = [str(exetutable)] + list(args)
    subprocess.run(cmd)


@cli.command()
@click.argument("text")
@click.argument("bold_text", default="")
def textbox(text, bold_text):
    print_text_box(text, bold_text)


@cli.command()
def version():
    """version of go4py"""
    print(metadata.version("go4py"))


@cli.command()
def py_include_path():
    """To be used as a -I flag"""
    print(sysconfig.get_path("include"))


@cli.command()
def py_lib_path():
    """To be used as a -L flag"""
    path = Path(sysconfig.get_config_var("installed_base"))

    file1 = path / "lib/libpython3.so"
    if file1.exists():
        print(str(file1.parent))

    file2 = path / "libs/python3.lib"
    if file2.exists():
        print(str(file2.parent))


if __name__ == "__main__":
    cli()
