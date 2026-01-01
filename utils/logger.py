from rich.console import Console

console = Console()

class Logger:
    @staticmethod
    def info(message: str):
        console.print(f"[bold blue][*][/bold blue] {message}")

    @staticmethod
    def success(message: str):
        console.print(f"[bold green][+][/bold green] {message}")

    @staticmethod
    def warning(message: str):
        console.print(f"[bold yellow][!][/bold yellow] {message}")

    @staticmethod
    def error(message: str):
        console.print(f"[bold red][-][/bold red] {message}")

    @staticmethod
    def debug(message: str):
        console.print(f"[grey50][DEBUG][/grey50] {message}")
