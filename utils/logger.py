from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.live import Live
from rich.panel import Panel

custom_theme = Theme({
    "info": "bold blue",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "debug": "grey50",
    "highlight": "bold cyan"
})

console = Console(theme=custom_theme)

class Logger:
    @staticmethod
    def info(message: str):
        console.print(f"[info][*][/info] {message}")

    @staticmethod
    def success(message: str):
        console.print(f"[success][+][/success] {message}")

    @staticmethod
    def warning(message: str):
        console.print(f"[warning][!][/warning] {message}")

    @staticmethod
    def error(message: str):
        console.print(f"[error][-][/error] {message}")

    @staticmethod
    def debug(message: str):
        console.print(f"[debug][DEBUG][/debug] {message}")

    @staticmethod
    def table(title: str, columns: list, rows: list):
        table = Table(title=title, show_header=True, header_style="bold magenta", border_style="highlight")
        for col in columns:
            table.add_column(col)
        for row in rows:
            table.add_row(*row)
        console.print(table)

    @staticmethod
    def get_progress():
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None, style="highlight"),
            TaskProgressColumn(),
            console=console
        )
