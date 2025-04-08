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
        Create a directory structure for a task and copy the input file.
        
        Args:
            input_file_path: Path to the input file
            
        Returns:
            Tuple containing:
            - task_id: Unique identifier for the task
            - input_dir: Directory containing the input file
            - input_file_name: Name of the copied input file
        """
        # Generate a unique task ID
        task_id = str(uuid.uuid4())
        
        # Create a directory for this task
        task_dir = self.base_dir / task_id
        task_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        input_dir = task_dir / "input"
        output_dir = task_dir / "output"
        qa_dir = task_dir / "qa_pairs"
        
        input_dir.mkdir(exist_ok=True)
        output_dir.mkdir(exist_ok=True)
        qa_dir.mkdir(exist_ok=True)
        
        # Copy the input file to the input directory
        input_path = Path(input_file_path)
        input_file_name = input_path.name
        shutil.copy2(input_path, input_dir / input_file_name)
        
        return task_id, str(input_dir / input_file_name), input_file_name
    
    def get_output_path(self, task_id: str, output_file_name: str) -> str:
        """Get the path for an output file."""
        output_dir = self.base_dir / task_id / "output"
        return str(output_dir / output_file_name)
    
    def get_qa_path(self, task_id: str, chunk_index: int) -> str:
        """Get the path for a Q&A pair file."""
        qa_dir = self.base_dir / task_id / "qa_pairs"
        return str(qa_dir / f"chunk_{chunk_index}.json")
    
    def save_qa_pair(self, task_id: str, chunk_index: int, qa_data: dict) -> str:
        """Save a Q&A pair to a JSON file."""
        import json
        qa_path = self.get_qa_path(task_id, chunk_index)
        with open(qa_path, 'w', encoding='utf-8') as f:
            json.dump(qa_data, f, indent=2)
        return qa_path
    
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
            
        input_files = list((task_dir / "input").glob("*"))
        output_files = list((task_dir / "output").glob("*"))
        qa_files = list((task_dir / "qa_pairs").glob("*.json"))
        
        return {
            "task_id": task_id,
            "input_files": [f.name for f in input_files],
            "output_files": [f.name for f in output_files],
            "qa_pairs": len(qa_files)
        } 