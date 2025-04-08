# Chapter Rewriter

A command-line application that helps students understand their textbooks and teacher's notes by rewriting them in a more understandable way. This version is in test mode and uses mock responses.

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The application provides three main commands:

1. Add a new task:
```bash
python -m chapter_rewriter.cli add-task input_file.md output_file.md
```

2. List all tasks:
```bash
python -m chapter_rewriter.cli list-tasks
```

3. Process pending tasks:
```bash
python -m chapter_rewriter.cli process-tasks
```

## Example

1. Create a markdown file with your chapter content (e.g., `chapter1.md`)
2. Add a task to rewrite it:
```bash
python -m chapter_rewriter.cli add-task chapter1.md rewritten_chapter1.md
```
3. Process the task:
```bash
python -m chapter_rewriter.cli process-tasks
```
4. Check the status of your tasks:
```bash
python -m chapter_rewriter.cli list-tasks
```

## Features

- Task queuing system for batch processing
- Persistent task storage
- Mock responses for testing
- Rich command-line interface
- Markdown output format

## Note

This is a test version that uses mock responses. In a production version, it would integrate with a real LLM API to generate the rewritten content. 