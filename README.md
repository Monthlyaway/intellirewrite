
# 📚 IntelliRewrite: AI-Powered Text Rewriter

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Monthlyaway/intellirewrite.svg)](https://github.com/Monthlyaway/intellirewrite/stargazers)
[![Issues](https://img.shields.io/github/issues/Monthlyaway/intellirewrite.svg)](https://github.com/Monthlyaway/intellirewrite/issues)

[toc]

## 🚀 What is IntelliRewrite?

IntelliRewrite is a powerful command-line tool that helps students, researchers, and writers improve their text by using AI to rewrite content while preserving the original meaning. It's perfect for:

- 📝 Rewriting notes and essays
- 🔄 Improving the clarity and flow of your writing
- 📚 Processing large documents in manageable chunks
- 🌐 Supporting multiple AI providers through configurable endpoints

## ✨ Key Features

- **Task Management**: Queue-based system for handling multiple rewriting tasks
- **Smart Chunking**: Process large documents in manageable pieces
- **Flexible API Support**: Works with OpenAI APIs
- **Memory Context**: Maintain consistency across chunks with configurable memory
- **Progress Tracking**: Real-time progress updates with detailed information
- **Resumable Processing**: Continue interrupted tasks without losing progress

## 🌍 Global Accessibility

IntelliRewrite is designed to work worldwide:

- **Multiple API Endpoints**: Configure different base URLs for regional access
- **International Users**: Use `https://api.siliconflow.cn/v1` for better connectivity
- **Chinese Users**: Use `https://api.deepseek.com/v1`

## 📚 Supported Formats

- **Markdown**: `.md`
- **Text**: `.txt`

❌ **PDF**:  `.pdf` (not supported) use [MinerU](https://github.com/opendatalab/MinerU) to extract text from PDF


## 🔄 Workflow Overview

### Standard Processing Flow
1. **Add Tasks**  
   Queue documents for processing:
   ```bash
   python -m chapter_rewriter.cli add-task document1.md
   python -m chapter_rewriter.cli add-task document2.txt
   ```

2. **Monitor Queue**  
   View pending tasks:
   ```bash
   python -m chapter_rewriter.cli list-tasks
   ```
   Sample Output:
   ```
   Task ID | Status    | Progress | File
   ----------------------------------------
   1       | PENDING   | 0%       | document1.md
   2       | QUEUED    | 0%       | document2.txt
   ```

3. **Process Tasks**  
   Start AI-powered rewriting:
   ```bash
   python -m chapter_rewriter.cli process-tasks
   ```
   Real-time updates:
   ```
   Processing document1.md [■■■■□□□□□□] 40%
   Current chunk: 12/30 (1024 chars)
   Estimated remaining: 8m 23s
   ```

Output files are in folder `output`

### Key Workflow Features
- **Batch Processing**: Add multiple files before processing
- **Priority Queue**: Tasks are processed in added order
- **Progress Saving**: Resume interrupted tasks automatically
- **Output Structure**: Preserves original document hierarchy



## 🔧 Chunk Size Configuration

**Default:** 800 characters (including spaces)

### Why Character Count?
We use character-based chunking to ensure fair calculation across languages:
- English: Spaces are integral to word separation
- Chinese: Rarely uses spaces between words
- Mixed content: Provides consistent measurement

### Token Estimation Guide
| Language      | Characters | Token Estimate | Recommended Chunk Size |
|---------------|------------|----------------|------------------------|
| English       | 1000       | ~300 tokens    | 1200-1800 characters   |
| Chinese       | 1000       | ~600 tokens    | 500-1000 characters    |
| Mixed Content | 1000       | Varies         | 800-1200 characters    |

**Implementation Notes:**
1. Chunks always end at paragraph breaks (`\n\n`)
2. Actual chunk sizes may vary from estimates
3. Command-line estimates help prevent API overuse

**Example Configuration:**
```bash
# Chinese-dominated content
python -m chapter_rewriter.cli add-task --chunk-size 600 paper.md

# English technical document
python -m chapter_rewriter.cli add-task --chunk-size 1500 thesis.txt
```

---




## 🛠️ Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/Monthlyaway/intellirewrite.git
cd intellirewrite

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

Edit the `.env` file with your API key and preferred settings:

```
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com  # Change to https://api.siliconflow.cn/v1 if needed
```

## 📖 Usage

### Basic Usage

```bash
# Add a task to the queue
python -m chapter_rewriter.cli add-task input.md

# Process all pending tasks
python -m chapter_rewriter.cli process-tasks
```

### Advanced Options

```bash
# Add a task with custom chunk size and memory context
python -m chapter_rewriter.cli add-task --chunk-size 300 --memory-size 3 input.md

# List all tasks
python -m chapter_rewriter.cli list-tasks

# Show details of a specific task
python -m chapter_rewriter.cli show-task task_id
```

For more details, please refer to the manual page:

```bash
python -m chapter_rewriter.cli --help
python -m chapter_rewriter.cli add-task --help
python -m chapter_rewriter.cli process-tasks --help
python -m chapter_rewriter.cli list-tasks --help
python -m chapter_rewriter.cli show-task --help
```

## 🎓 Perfect for Students

IntelliRewrite is designed with students in mind:

- **Study Notes**: Rewrite your notes for better clarity and understanding
- **Essay Improvement**: Enhance your writing without changing the meaning
- **Research Papers**: Process and improve large academic documents
- **Language Learning**: See how AI rewrites text to improve your language skills

## 🔧 Configuration

### Environment Variables

- `DEEPSEEK_API_KEY`: Your API key
- `DEEPSEEK_BASE_URL`: API base URL (change for regional access)

### Task-Specific Settings

Each task can have its own settings stored in `task.json`:

- `chunk_size`: Size of text chunks to process
- `memory_size`: Number of previous chunks to include for context


## 🙏 Acknowledgments

- Thanks to all contributors who have helped improve IntelliRewrite
- Special thanks to the open-source community for inspiration and tools

---

<div align="center">
  <p>Made with ❤️ for students and writers worldwide</p>
</div> 