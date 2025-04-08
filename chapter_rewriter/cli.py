import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from .queue_manager import QueueManager
from .models import TaskStatus

app = typer.Typer()
console = Console()
queue_manager = QueueManager()

@app.command()
def add_task(input_file: str, output_file: str):
    """Add a new chapter rewriting task to the queue."""
    if not Path(input_file).exists():
        console.print(f"[red]Error: Input file '{input_file}' does not exist.[/red]")
        raise typer.Exit(1)

    task = queue_manager.add_task(input_file, output_file)
    console.print(f"[green]Task added successfully![/green]")
    console.print(f"Task ID: {task.id}")
    console.print(f"Status: {task.status}")

@app.command()
def list_tasks():
    """List all tasks in the queue."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Task ID")
    table.add_column("Input File")
    table.add_column("Output File")
    table.add_column("Status")
    table.add_column("Created At")

    for task in queue_manager.tasks:
        table.add_row(
            task.id,
            task.input_file,
            task.output_file,
            task.status,
            task.created_at.strftime("%Y-%m-%d %H:%M:%S")
        )

    console.print(table)

@app.command()
def process_tasks():
    """Process all pending tasks in the queue."""
    pending_tasks = queue_manager.get_pending_tasks()
    if not pending_tasks:
        console.print("[yellow]No pending tasks to process.[/yellow]")
        return

    for task in pending_tasks:
        console.print(f"Processing task {task.id}...")
        try:
            # In test mode, we just write the mock response
            with open(task.output_file, 'w') as f:
                f.write(task.mock_response)
            queue_manager.update_task_status(task.id, TaskStatus.COMPLETED)
            console.print(f"[green]Task {task.id} completed successfully![/green]")
        except Exception as e:
            queue_manager.update_task_status(task.id, TaskStatus.FAILED, str(e))
            console.print(f"[red]Task {task.id} failed: {str(e)}[/red]")

if __name__ == "__main__":
    app() 