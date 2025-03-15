from rich.console import Console
from rich.panel import Panel

console = Console()


def print_text_box(text, bold_text=""):
    if bold_text:
        text += f"  [bold]{bold_text}[/bold] "
    panel = Panel(f" {text} ", title_align="center", border_style="green", expand=False)
    console.print(panel)


if __name__ == "__main__":
    print_text_box("hi", "wed")

"""
uv run -m go4py.utils.text_util
"""
