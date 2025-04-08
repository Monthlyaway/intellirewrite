# DeepSeek Chapter Rewriter

A command-line tool for rewriting book chapters using the DeepSeek API. This tool processes text files, breaks them into manageable chunks, and uses the DeepSeek API to rewrite each chunk while maintaining the original meaning and style.

## Features

- Process large text files in chunks
- Queue-based task management
- Progress tracking with visual feedback
- Configurable processing parameters
- Organized output with Q&A pairs
- Error handling and retry mechanisms
- Memory context for improved continuity between chunks

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/deepseek-rewrite.git
cd deepseek-rewrite
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```
Edit the `.env` file with your DeepSeek API key and other configuration options.

## Usage

### Basic Usage

```bash
python -m chapter_rewriter.cli add-task input.txt output.txt
python -m chapter_rewriter.cli process-tasks
```

### Command Line Options

#### Add Task
- `--chunk-size`: Size of text chunks to process (default: 500)
- `--memory-size`: Number of previous Q&A pairs to include in the prompt (default: 0)

#### Process Tasks
- `--max-retries`: Maximum number of API retry attempts (default: 3)
- `--timeout`: API request timeout in seconds (default: 30)
- `--output-dir`: Directory for output files (default: "output")

### Examples

Add a task with custom chunk size and memory size:
```bash
python -m chapter_rewriter.cli add-task --chunk-size 2000 --memory-size 3 input.txt output.txt
```

Process all pending tasks:
```bash
python -m chapter_rewriter.cli process-tasks
```

List all tasks:
```bash
python -m chapter_rewriter.cli list-tasks
```

Show details of a specific task:
```bash
python -m chapter_rewriter.cli show-task task_id
```

## Project Structure

```
chapter_rewriter/
├── __init__.py
├── cli.py              # Command-line interface
├── config.py           # Configuration management
├── models.py           # Data models
├── queue_manager.py    # Task queue management
├── text_processor.py   # Text processing logic
└── utils.py            # Utility functions
```

## Configuration

The following environment variables can be configured in the `.env` file:

- `DEEPSEEK_API_KEY`: Your DeepSeek API key
- `DEEPSEEK_BASE_URL`: DeepSeek API base URL
- `MAX_RETRIES`: Maximum number of API retry attempts
- `TIMEOUT_SECONDS`: API request timeout in seconds

Task-specific parameters (chunk_size, memory_size) are stored in the task.json file within each task's directory.

## Error Handling

The tool includes comprehensive error handling:
- API request failures are retried automatically
- Failed tasks are marked and can be reprocessed
- Detailed error messages are provided for debugging
- Graceful handling of models without reasoning_content

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 