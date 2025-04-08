import os
import shutil
from pathlib import Path
from typing import Tuple, Optional
import uuid

class FileManager:
    def __init__(self, base_dir: str = "chapter_data"):
        """Initialize the file manager with a base directory for all data."""
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        
    def create_task_directory(self, input_file_path: str) -> Tuple[str, str, str]:
        """
        Create a directory for a task and copy the input file.
        
        Args:
            input_file_path: Path to the input file
            
        Returns:
            Tuple containing:
            - task_id: Unique identifier for the task
            - input_file_path: Path to the copied input file
            - input_file_name: Name of the copied input file
        """
        # Generate a unique task ID
        task_id = str(uuid.uuid4())
        
        # Create a directory for this task
        task_dir = self.base_dir / task_id
        task_dir.mkdir(exist_ok=True)
        
        # Copy the input file to the task directory
        input_path = Path(input_file_path)
        input_file_name = input_path.name
        shutil.copy2(input_path, task_dir / input_file_name)
        
        return task_id, str(task_dir / input_file_name), input_file_name
    
    def get_output_path(self, task_id: str, output_file_name: str) -> str:
        """Get the path for an output file."""
        task_dir = self.base_dir / task_id
        return str(task_dir / output_file_name)
    
    def get_chunks_file(self, task_id: str) -> str:
        """Get the path for the chunks JSON file."""
        task_dir = self.base_dir / task_id
        return str(task_dir / "chunks.json")
    
    def get_qa_json_path(self, task_id: str) -> str:
        """Get the path for the Q&A pairs JSON file."""
        task_dir = self.base_dir / task_id
        return str(task_dir / "qa_pairs.json")
    
    def get_task_directory(self, task_id: str) -> Optional[Path]:
        """Get the directory for a task if it exists."""
        task_dir = self.base_dir / task_id
        if task_dir.exists():
            return task_dir
        return None
    
    def list_tasks(self) -> list:
        """List all task directories."""
        return [d.name for d in self.base_dir.iterdir() if d.is_dir()]
    
    def get_task_info(self, task_id: str) -> dict:
        """Get information about a task."""
        task_dir = self.get_task_directory(task_id)
        if not task_dir:
            return {}
            
        input_files = list(task_dir.glob("*.*"))
        
        return {
            "task_id": task_id,
            "input_files": [f.name for f in input_files if f.name != "chunks.json" and f.name != "qa_pairs.json"],
            "has_chunks": (task_dir / "chunks.json").exists(),
            "has_qa_pairs": (task_dir / "qa_pairs.json").exists()
        } 