import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from .queue_manager import QueueManager
from .models import TaskStatus, QAPair
from .text_processor import TextProcessor
import json

app = typer.Typer()
console = Console()
queue_manager = QueueManager()
text_processor = TextProcessor(chunk_size=500)  # Default chunk size of 500 words

@app.command()
def add_task(input_file: str, output_file: str, chunk_size: int = 500):
    """Add a new chapter rewriting task to the queue."""
    if not Path(input_file).exists():
        console.print(f"[red]Error: Input file '{input_file}' does not exist.[/red]")
        raise typer.Exit(1)

    # Process the file to get chunks
    chunks = text_processor.process_file(input_file)
    
    task = queue_manager.add_task(input_file, output_file)
    task.total_chunks = len(chunks)
    task.processed_chunks = 0
    queue_manager._save_tasks()

    console.print(f"[green]Task added successfully![/green]")
    console.print(f"Task ID: {task.id}")
    console.print(f"Directory ID: {task.task_id}")
    console.print(f"Status: {task.status}")
    console.print(f"Total chunks: {task.total_chunks}")
    console.print(f"Input file: {task.input_file}")
    console.print(f"Output file: {task.output_file}")

@app.command()
def list_tasks():
    """List all tasks in the queue."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Task ID")
    table.add_column("Directory ID")
    table.add_column("Input File")
    table.add_column("Output File")
    table.add_column("Status")
    table.add_column("Progress")
    table.add_column("Created At")

    for task in queue_manager.tasks:
        progress = f"{task.processed_chunks}/{task.total_chunks}" if task.total_chunks > 0 else "N/A"
        table.add_row(
            task.id,
            task.task_id,
            Path(task.input_file).name,
            Path(task.output_file).name,
            task.status,
            progress,
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
            # Update task status to processing
            queue_manager.update_task_status(task.id, TaskStatus.PROCESSING)
            
            # Process the file in chunks
            chunks = text_processor.process_file(task.input_file)
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task_progress = progress.add_task(
                    f"Processing chunks for {Path(task.input_file).name}...", 
                    total=len(chunks)
                )
                
                # Process each chunk
                for i, chunk in enumerate(chunks):
                    # In test mode, we use the mock response for each chunk
                    qa_pair = QAPair(
                        question=chunk.content,
                        answer=task.mock_response,  # In real implementation, this would be the API response
                        chunk_index=i,
                        word_count=chunk.word_count
                    )
                    
                    # Save the Q&A pair to a file using task_id
                    qa_data = qa_pair.model_dump()
                    qa_path = queue_manager.file_manager.save_qa_pair(task.task_id, i, qa_data)
                    qa_pair.file_path = qa_path
                    
                    task.qa_pairs.append(qa_pair)
                    task.processed_chunks += 1
                    progress.update(task_progress, advance=1)
                    queue_manager._save_tasks()

            # Write the final output using task_id for the output path
            output_path = queue_manager.file_manager.get_output_path(task.task_id, Path(task.output_file).name)
            with open(output_path, 'w', encoding='utf-8') as f:
                for qa in task.qa_pairs:
                    f.write(f"## Original Text (Chunk {qa.chunk_index + 1})\n\n")
                    f.write(qa.question)
                    f.write("\n\n")
                    f.write("## Rewritten Version\n\n")
                    f.write(qa.answer)
                    f.write("\n\n---\n\n")

            queue_manager.update_task_status(task.id, TaskStatus.COMPLETED)
            console.print(f"[green]Task {task.id} completed successfully![/green]")
            console.print(f"Output saved to: {output_path}")
            
        except Exception as e:
            queue_manager.update_task_status(task.id, TaskStatus.FAILED, str(e))
            console.print(f"[red]Task {task.id} failed: {str(e)}[/red]")

@app.command()
def show_task(task_id: str):
    """Show detailed information about a specific task."""
    task = queue_manager.get_task(task_id)
    if not task:
        console.print(f"[red]Task with ID {task_id} not found.[/red]")
        return
    
    console.print(f"[bold]Task Information:[/bold]")
    console.print(f"ID: {task.id}")
    console.print(f"Directory ID: {task.task_id}")
    console.print(f"Status: {task.status}")
    console.print(f"Created: {task.created_at}")
    if task.completed_at:
        console.print(f"Completed: {task.completed_at}")
    console.print(f"Input File: {task.input_file}")
    console.print(f"Output File: {task.output_file}")
    console.print(f"Progress: {task.processed_chunks}/{task.total_chunks} chunks")
    
    if task.error_message:
        console.print(f"[red]Error: {task.error_message}[/red]")
    
    # Show Q&A pairs
    if task.qa_pairs:
        console.print(f"\n[bold]Q&A Pairs:[/bold]")
        for i, qa in enumerate(task.qa_pairs):
            console.print(f"\n[bold]Chunk {i+1}:[/bold]")
            console.print(f"Word Count: {qa.word_count}")
            console.print(f"File: {qa.file_path}")
            
            # Show a preview of the content
            question_preview = qa.question[:100] + "..." if len(qa.question) > 100 else qa.question
            console.print(f"Question Preview: {question_preview}")
    
    # Show directory structure
    task_dir = queue_manager.get_task_directory(task_id)
    if task_dir:
        console.print(f"\n[bold]Directory Structure:[/bold]")
        console.print(f"Base Directory: {task_dir}")
        
        # List files in each subdirectory
        for subdir in ["input", "output", "qa_pairs"]:
            subdir_path = task_dir / subdir
            if subdir_path.exists():
                files = list(subdir_path.glob("*"))
                console.print(f"{subdir}: {len(files)} files")
                for file in files:
                    console.print(f"  - {file.name}")

if __name__ == "__main__":
    app() 