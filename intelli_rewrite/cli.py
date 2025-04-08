import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from .queue_manager import QueueManager
from .models import TaskStatus, QAPair
from .text_processor import TextProcessor
from .api_client import DeepSeekAPI
import json
import os

app = typer.Typer()
console = Console()
queue_manager = QueueManager()
text_processor = None  # Initialize as None, will be created with proper chunk size
api_client = None  # Initialize as None, will be created when needed

@app.command()
def add_task(
    input_file: str, 
    output_file: str = None, 
    chunk_size: int = typer.Option(800, help="Size of text chunks to process"),
    memory_size: int = typer.Option(0, help="Number of previous Q&A pairs to include in the prompt (0 for no memory)")
):
    """Add a new chapter rewriting task to the queue."""
    if not Path(input_file).exists():
        console.print(f"[red]Error: Input file '{input_file}' does not exist.[/red]")
        raise typer.Exit(1)

    # Generate default output file name if not provided
    if output_file is None:
        input_path = Path(input_file)
        output_file = f"rewritten_{input_path.stem}.md"
        console.print(f"[yellow]No output file specified. Using default: {output_file}[/yellow]")

    # Create the task with the specified parameters
    task = queue_manager.add_task(
        input_file=input_file, 
        output_file=output_file,
        chunk_size=chunk_size,
        memory_size=memory_size
    )
    
    # Initialize text processor with the specified chunk size
    global text_processor
    text_processor = TextProcessor(chunk_size=chunk_size)

    # Process the file to get chunks
    chunks = text_processor.process_file(input_file)
    
    # Update task with chunk information
    task.total_chunks = len(chunks)
    task.processed_chunks = 0
    
    # Store chunks in JSON
    chunks_data = []
    for i, chunk in enumerate(chunks):
        chunks_data.append({
            "index": i,
            "content": chunk.content,
            "start_line": chunk.start_line,
            "end_line": chunk.end_line,
            "char_count": chunk.char_count
        })
    
    # Save chunks to a JSON file
    chunks_file = queue_manager.file_manager.get_chunks_file(task.task_id)
    with open(chunks_file, 'w', encoding='utf-8') as f:
        json.dump(chunks_data, f, ensure_ascii=False, indent=2)
    
    queue_manager._save_tasks()

    console.print(f"[green]Task added successfully![/green]")
    console.print(f"Task ID: {task.id}")
    console.print(f"Directory ID: {task.task_id}")
    console.print(f"Status: {task.status}")
    console.print(f"Total chunks: {task.total_chunks}")
    console.print(f"Input file: {task.input_file}")
    console.print(f"Output file: {task.output_file}")
    console.print(f"Chunk size: {chunk_size} characters")
    console.print(f"Memory size: {memory_size} previous chunks")
    console.print(f"Chunks saved to: {chunks_file}")

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
    table.add_column("Chunk Size")
    table.add_column("Memory Size")
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
            str(task.chunk_size),
            str(task.memory_size),
            task.created_at.strftime("%Y-%m-%d %H:%M:%S")
        )

    console.print(table)

@app.command()
def process_tasks():
    """Process all pending tasks in the queue."""
    # Initialize API client if not already done
    global api_client
    if api_client is None:
        try:
            api_client = DeepSeekAPI()
            console.print("[green]Successfully connected to DeepSeek API[/green]")
        except Exception as e:
            console.print(f"[red]Error initializing DeepSeek API: {str(e)}[/red]")
            console.print("[yellow]Using mock responses instead[/yellow]")
            api_client = None
            return
    
    # Get pending tasks
    pending_tasks = queue_manager.get_pending_tasks()
    if not pending_tasks:
        console.print("[yellow]No pending tasks to process.[/yellow]")
        return
    
    # Check for interrupted tasks
    interrupted_tasks = [task for task in pending_tasks if task.processed_chunks > 0]
    if interrupted_tasks:
        console.print(f"[yellow]Found {len(interrupted_tasks)} interrupted task(s). Resuming...[/yellow]")
        for task in interrupted_tasks:
            console.print(f"  - Task {task.id}: {Path(task.input_file).name} ({task.processed_chunks}/{task.total_chunks} chunks processed)")
    
    for task in pending_tasks:
        try:
            # Update task status to processing
            queue_manager.update_task_status(task.id, TaskStatus.PROCESSING)
            
            # Get the chunks file path
            chunks_file = queue_manager.file_manager.get_chunks_file(task.task_id)
            qa_json_path = queue_manager.file_manager.get_qa_json_path(task.task_id)
            
            # Load chunks
            with open(chunks_file, 'r', encoding='utf-8') as f:
                chunks_data = json.load(f)
                
            # Update total chunks count
            task.total_chunks = len(chunks_data)
            
            # Load existing Q&A pairs if any
            if Path(qa_json_path).exists():
                with open(qa_json_path, 'r', encoding='utf-8') as f:
                    existing_qa_pairs = json.load(f)
                    # Convert to QAPair objects
                    task.qa_pairs = [QAPair(**qa) for qa in existing_qa_pairs]
            
            # Get the output file path
            output_path = queue_manager.file_manager.get_output_path(task.task_id, Path(task.output_file).name)
            
            # Check if we're resuming a task
            is_resuming = task.processed_chunks > 0
            
            # If resuming, don't clear the output file
            if not is_resuming:
                # Create or clear the output file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write("")  # Clear the file
            else:
                # For resumed tasks, ensure the output file exists
                if not Path(output_path).exists():
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write("")  # Create the file if it doesn't exist
            
            # Display task information
            console.print(f"[bold cyan]Processing Task:[/bold cyan]")
            console.print(f"Task ID: {task.id}")
            console.print(f"Directory ID: {task.task_id}")
            console.print(f"Input File: {Path(task.input_file).name}")
            console.print(f"Output File: {Path(task.output_file).name}")
            console.print(f"Total Chunks: {task.total_chunks}")
            console.print(f"Processed Chunks: {task.processed_chunks}")
            console.print(f"Memory Size: {task.memory_size}")
            console.print(f"Output Path: {output_path}")
            console.print(f"Q&A Path: {qa_json_path}")
            if is_resuming:
                console.print(f"[yellow]Resuming task from chunk {task.processed_chunks + 1}[/yellow]")
            console.print("")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                task_progress = progress.add_task(
                    f"Processing {Path(task.input_file).name} ({task.processed_chunks}/{task.total_chunks})", 
                    total=task.total_chunks,
                    completed=task.processed_chunks
                )
                
                # Process each chunk
                for i, chunk_data in enumerate(chunks_data):
                    content = chunk_data["content"]
                    chunk_index = chunk_data["index"]
                    char_count = chunk_data["char_count"]
                    
                    # Update progress description with current chunk information
                    progress.update(
                        task_progress, 
                        description=f"Task {task.id} - Chunk {i+1}/{task.total_chunks} ({char_count} chars)"
                    )
                    
                    # Skip if this chunk was already processed
                    if any(qa.chunk_index == chunk_index for qa in task.qa_pairs):
                        progress.update(task_progress, advance=1)
                        continue
                    
                    # Get memory context if needed
                    memory_context = []
                    if task.memory_size > 0:
                        # Get previous Q&A pairs for context
                        start_idx = max(0, i - task.memory_size)
                        memory_pairs = task.qa_pairs[start_idx:i]
                        if memory_pairs:
                            # Convert Q&A pairs to message format
                            for qa in memory_pairs:
                                memory_context.append({"role": "user", "content": qa.question})
                                memory_context.append({"role": "assistant", "content": qa.answer})
                    
                    try:
                        # Generate response
                        response = api_client.generate_response(content, memory_context)
                        
                        # Get the content and reasoning from the response
                        content = response.get("content", "")
                        reasoning = response.get("reasoning_content")
                        
                        # Create Q&A pair
                        qa_pair = QAPair(
                            question=content,
                            answer=content,
                            reasoning_content=reasoning,
                            chunk_index=chunk_index,
                            char_count=char_count
                        )
                        
                        # Add the Q&A pair to the task
                        task.qa_pairs.append(qa_pair)
                        task.processed_chunks += 1
                        
                        # Save Q&A pairs after each chunk is processed
                        with open(qa_json_path, 'w', encoding='utf-8') as f:
                            json.dump([qa.model_dump() for qa in task.qa_pairs], f, ensure_ascii=False, indent=2)
                        
                        # Append the rewritten content to the output file in real-time
                        with open(output_path, 'a', encoding='utf-8') as f:
                            f.write(content)
                            f.write("\n\n")
                    except Exception as e:
                        console.print(f"[red]Error processing chunk {i+1}: {str(e)}[/red]")
                        # Create a placeholder Q&A pair for this chunk
                        qa_pair = QAPair(
                            question=content,
                            answer=f"[Error: {str(e)}]",
                            reasoning_content=f"Error processing chunk: {str(e)}",
                            chunk_index=chunk_index,
                            char_count=char_count
                        )
                        task.qa_pairs.append(qa_pair)
                        task.processed_chunks += 1
                        
                        # Save Q&A pairs after each chunk is processed
                        with open(qa_json_path, 'w', encoding='utf-8') as f:
                            json.dump([qa.model_dump() for qa in task.qa_pairs], f, ensure_ascii=False, indent=2)
                        
                        # Append the error message to the output file
                        with open(output_path, 'a', encoding='utf-8') as f:
                            f.write(f"[Error processing chunk: {str(e)}]")
                            f.write("\n\n")
                    
                    progress.update(task_progress, advance=1)
                    
                    # Save task status
                    queue_manager._save_tasks()

            queue_manager.update_task_status(task.id, TaskStatus.COMPLETED)
            console.print(f"[green]Task {task.id} completed successfully![/green]")
            console.print(f"Output saved to: {output_path}")
            console.print(f"Q&A pairs saved to: {qa_json_path}")
            
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
    console.print(f"Chunk Size: {task.chunk_size}")
    console.print(f"Memory Size: {task.memory_size}")
    
    if task.error_message:
        console.print(f"[red]Error: {task.error_message}[/red]")
    
    # Show Q&A pairs
    if task.qa_pairs:
        console.print(f"\n[bold]Q&A Pairs:[/bold]")
        for i, qa in enumerate(task.qa_pairs):
            console.print(f"\n[bold]Chunk {i+1}:[/bold]")
            console.print(f"Character Count: {qa.char_count}")
            
            # Show a preview of the content
            question_preview = qa.question[:100] + "..." if len(qa.question) > 100 else qa.question
            console.print(f"Question Preview: {question_preview}")
    
    # Show directory structure
    task_dir = queue_manager.get_task_directory(task_id)
    if task_dir:
        console.print(f"\n[bold]Directory Structure:[/bold]")
        console.print(f"Base Directory: {task_dir}")
        
        # List files in the task directory
        files = list(task_dir.glob("*"))
        console.print(f"Files: {len(files)}")
        for file in files:
            console.print(f"  - {file.name}")

if __name__ == "__main__":
    app() 