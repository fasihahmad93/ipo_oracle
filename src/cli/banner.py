import pyfiglet

from rich.console import Console
from rich.panel import Panel


console = Console()


def display_cli_banner() -> None:
    banner = pyfiglet.figlet_format(
        "IPO ORACLE",
        font="slant",
    )

    console.print(
        Panel(
            banner,
            subtitle="AI-Powered IPO Intelligence",
            border_style="cyan",
        )
    )