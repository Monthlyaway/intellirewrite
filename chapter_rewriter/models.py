from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Dict

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class QAPair(BaseModel):
    question: str
    answer: str
    chunk_index: int
    char_count: int

class RewriteTask(BaseModel):
    id: str
    task_id: str  # Directory ID for file organization
    input_file: str
    output_file: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = datetime.now()
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    qa_pairs: List[QAPair] = []
    total_chunks: int = 0
    processed_chunks: int = 0
    mock_response: str = """
# Rewritten Chapter

This is a mock response that would normally come from an LLM API.
The actual implementation would make an API call to get this content.

## Key Concepts

1. First important point
2. Second important point
3. Third important point

## Detailed Explanation

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor 
incididunt ut labore et dolore magna aliqua.

### Mathematical Explanation

For any given equation:
```
E = mc²
```
This represents the relationship between energy and mass.
""" 