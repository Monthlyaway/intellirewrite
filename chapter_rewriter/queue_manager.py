import json
import uuid
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from .models import RewriteTask, TaskStatus

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class QueueManager:
    def __init__(self, queue_file: str = "tasks.json"):
        self.queue_file = Path(queue_file)
        self.tasks: List[RewriteTask] = []
        self._load_tasks()

    def _load_tasks(self):
        if self.queue_file.exists():
            with open(self.queue_file, 'r') as f:
                data = json.load(f)
                self.tasks = [RewriteTask(**task) for task in data]

    def _save_tasks(self):
        with open(self.queue_file, 'w') as f:
            json.dump([task.model_dump() for task in self.tasks], f, indent=2, cls=DateTimeEncoder)

    def add_task(self, input_file: str, output_file: str) -> RewriteTask:
        task = RewriteTask(
            id=str(uuid.uuid4()),
            input_file=input_file,
            output_file=output_file
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