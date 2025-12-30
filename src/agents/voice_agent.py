"""Voice agent for experimental voice command support.

Handles listening for and processing voice commands to interact with the application.
"""
from rich.console import Console

console = Console()

def activate_voice_mode() -> None:
    """Activate voice command mode and listen for input."""
    console.print("[bold yellow]Voice Command Mode active (Experimental)...[/bold yellow]")
    console.print("[cyan]Listening...[/cyan]")
    console.print("[blue]Feature coming soon. This will allow you to add and manage tasks via voice.[/blue]")

def get_voice_status() -> str:
    """Return the status of the voice agent."""
    return "Voice agent is in experimental phase."
