from dataclasses import dataclass
from typing import List, Tuple
import re

@dataclass
class TextChunk:
    content: str
    start_line: int
    end_line: int
    word_count: int

class TextProcessor:
    def __init__(self, chunk_size: int = 500):
        self.chunk_size = chunk_size

    def _count_words(self, text: str) -> int:
        # Simple word counting - split by whitespace and count non-empty strings
        return len([w for w in text.split() if w.strip()])

    def _find_chunk_boundary(self, lines: List[str], target_words: int) -> Tuple[int, int]:
        """Find the line index where we should end the chunk based on word count."""
        current_words = 0
        for i, line in enumerate(lines):
            line_words = self._count_words(line)
            if current_words + line_words > target_words:
                # If this is the first line and it already exceeds target, we need to include it
                if i == 0:
                    return 0, 0
                # Otherwise, return the previous line index
                return i - 1, current_words
            current_words += line_words
        # If we've gone through all lines, return the last line
        return len(lines) - 1, current_words

    def split_into_chunks(self, text: str) -> List[TextChunk]:
        """Split text into chunks of approximately chunk_size words, respecting paragraph boundaries."""
        lines = text.split('\n')
        chunks = []
        current_line = 0

        while current_line < len(lines):
            # Find where this chunk should end
            end_line, word_count = self._find_chunk_boundary(
                lines[current_line:], 
                self.chunk_size
            )
            
            # Adjust end_line to be relative to the full text
            end_line += current_line
            
            # Create the chunk
            chunk_content = '\n'.join(lines[current_line:end_line + 1])
            chunks.append(TextChunk(
                content=chunk_content,
                start_line=current_line,
                end_line=end_line,
                word_count=word_count
            ))
            
            # Move to the next line
            current_line = end_line + 1

        return chunks

    def process_file(self, file_path: str) -> List[TextChunk]:
        """Process a file and return its chunks."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return self.split_into_chunks(content) 