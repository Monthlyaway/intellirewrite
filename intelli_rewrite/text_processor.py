from dataclasses import dataclass
from typing import List

@dataclass
class TextChunk:
    content: str
    start_line: int
    end_line: int
    char_count: int

class TextProcessor:
    def __init__(self, chunk_size: int = 800):
        self.chunk_size = chunk_size

    def split_into_chunks(self, text: str) -> List[TextChunk]:
        """Split text into chunks of approximately chunk_size characters, respecting paragraph boundaries."""
        lines = text.split('\n')
        chunks = []
        current_line = 0
        total_lines = len(lines)

        while current_line < total_lines:
            # Start a new chunk
            chunk_start_line = current_line
            current_chars = 0
            chunk_end_line = current_line
            
            # Process lines until we reach the chunk size
            while current_line < total_lines:
                line = lines[current_line]
                line_chars = len(line)
                
                # If adding this line would exceed the chunk size, end the chunk here
                if current_chars + line_chars > self.chunk_size and current_chars > 0:
                    break
                
                # Add this line to the current chunk
                current_chars += line_chars
                chunk_end_line = current_line
                current_line += 1
            
            # If we didn't add any lines (empty lines), move to the next line
            if chunk_end_line < chunk_start_line:
                current_line += 1
                continue
                
            # Create the chunk
            chunk_content = '\n'.join(lines[chunk_start_line:chunk_end_line + 1])
            chunks.append(TextChunk(
                content=chunk_content,
                start_line=chunk_start_line,
                end_line=chunk_end_line,
                char_count=current_chars
            ))

        return chunks

    def process_file(self, file_path: str) -> List[TextChunk]:
        """Process a file and return its chunks."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return self.split_into_chunks(content) 