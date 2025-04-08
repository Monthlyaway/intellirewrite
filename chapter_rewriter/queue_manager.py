import json
import uuid
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from .models import RewriteTask, TaskStatus
from .file_manager import FileManager

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class QueueManager:
    def __init__(self, queue_file: str = "tasks.json"):
        self.queue_file = Path(queue_file)
        self.tasks: List[RewriteTask] = []
        self.file_manager = FileManager()
        self._load_tasks()

    def _load_tasks(self):
        if self.queue_file.exists():
            with open(self.queue_file, 'r') as f:
                data = json.load(f)
                # Handle transition: add task_id if missing
                for task_data in data:
                    if 'task_id' not in task_data:
                        # Generate a task_id for existing tasks
                        task_data['task_id'] = str(uuid.uuid4())
                self.tasks = [RewriteTask(**task) for task in data]

    def _save_tasks(self):
        with open(self.queue_file, 'w') as f:
            json.dump([task.model_dump() for task in self.tasks], f, indent=2, cls=DateTimeEncoder)

    def add_task(self, input_file: str, output_file: str) -> RewriteTask:
        # Create a directory structure for this task
        task_id, input_file_path, input_file_name = self.file_manager.create_task_directory(input_file)
        
        # Get the output file path
        output_file_path = self.file_manager.get_output_path(task_id, Path(output_file).name)
        
        task = RewriteTask(
            id=str(uuid.uuid4()),
            task_id=task_id,
            input_file=input_file_path,
            output_file=output_file_path
        )
        self.tasks.append(task)
        self._save_tasks()
        return task

    def get_task(self, task_id: str) -> Optional[RewriteTask]:
        return next((task for task in self.tasks if task.id == task_id), None)

    def get_pending_tasks(self) -> List[RewriteTask]:
        return [task for task in self.tasks if task.status == TaskStatus.PENDING]

    def update_task_status(self, task_id: str, status: TaskStatus, error_message: Optional[str] = None):
        task = self.get_task(task_id)
        if task:
            task.status = status
            if status == TaskStatus.COMPLETED:
                task.completed_at = datetime.now()
            if error_message:
                task.error_message = error_message
            self._save_tasks()
            
    def get_task_directory(self, task_id: str) -> Optional[Path]:
        """Get the directory for a task if it exists."""
        task = self.get_task(task_id)
        if task:
            return self.file_manager.get_task_directory(task.task_id)
        return None 