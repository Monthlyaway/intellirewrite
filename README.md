# 📚 IntelliRewrite: AI-Powered Text Rewriter

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/) [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Stars](https://img.shields.io/github/stars/Monthlyaway/intellirewrite.svg)](https://github.com/Monthlyaway/intellirewrite/stargazers) [![Issues](https://img.shields.io/github/issues/Monthlyaway/intellirewrite.svg)](https://github.com/Monthlyaway/intellirewrite/issues)

[English](README.md) | [中文](README.zh-CN.md)

## 🚀 What is IntelliRewrite?

IntelliRewrite is a powerful command-line tool that helps students, researchers, and writers improve their text by using AI to rewrite content while preserving the original meaning. It's perfect for:

- 📝 Rewriting notes and essays
- 🔄 Improving the clarity and flow of your writing
- 📚 Processing large documents in manageable chunks
- 🌐 Supporting multiple AI providers through configurable endpoints

### ✨ Key Features

- **Task Management**: Queue-based system for handling multiple rewriting tasks
- **Smart Chunking**: Process large documents in manageable pieces
- **Memory Context**: Maintain consistency across chunks with configurable memory
- **Flexible API Support**: Works with OpenAI APIs
- **Progress Tracking**: Real-time progress updates with detailed information
- **Resumable Processing**: Continue interrupted tasks without losing progress

### 🎓 Perfect for Students

IntelliRewrite is designed with students in mind:

- **Study Notes**: Rewrite your notes for better clarity and understanding
- **Essay Improvement**: Enhance your writing without changing the meaning
- **Research Papers**: Process and improve large academic documents
- **Language Learning**: See how AI rewrites text to improve your language skills

### 🌍 API Flexibility

IntelliRewrite supports any OpenAI-compatible API endpoint:

- **Custom Endpoints**: Configure your preferred API base URL
- **Multi-model Support**: Works with OpenAI, DeepSeek, and other compatible services. Deepseek-R1 has reasoning ability I heard? Sure! IntelliRewrite works just fine.


## 🔄 Workflow Overview

### 🎭 Real-World Example

Imagine this: Your Linear Algebra professor assigns Chapter 3 & 4 on "Eigenvalues and Eigenvectors" - you know, that chapter where suddenly matrices start having "personalities" and vectors get "special treatment."

You: *stares at textbook* "Wait, how did they jump from step 2 to step 7? Did I miss four pages?"

**Enter IntelliRewrite workflow:**

1. **Extract & Convert**  
   Convert that dense PDF to markdown using [MinerU](https://github.com/opendatalab/MinerU)

2. **Queue It Up**  
   ```bash
   python -m chapter_rewriter.cli add-task linear_algebra_ch3.md --chunk-size 800
    python -m chapter_rewriter.cli add-task linear_algebra_ch4.md --chunk-size 800

   ```

3. **Let AI Work Overnight**  
   ```bash
   python -m chapter_rewriter.cli process-tasks
   ```

4. **Next Morning**  
   Open `output/linear_algebra_ch3_rewritten.md` and  `output/linear_algebra_ch4_rewritten.md` and find a beautifully explained version that actually shows those missing steps and explains why eigenvalues matter in the real world!

   No more "it can be trivially shown that..." when there's nothing trivial about it!


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
   ```

Output files are in folder `output`

### Key Workflow Features
- **Batch Processing**: Add multiple files before processing (So you can hangout with your buds)
- **Priority Queue**: Tasks are processed in added order (Make sure your credit is enough)
- **Progress Saving**: Resume interrupted tasks automatically. Each task has a status: pending, processing, completed, failed. Tasks that are pending and processing will be resumed.



## 🔧 Chunk Size Configuration

Adjust how documents are split into manageable pieces for processing. Long documents are automatically chunked into smaller sections to optimize LLM processing. The `--chunk-size` parameter controls the approximate number of characters per chunk (not tokens), allowing you to fine-tune processing based on document complexity and language characteristics.



**Default:** 800 characters

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
API_KEY=your_api_key_here
BASE_URL=base_url_here
```

## 📖 Usage

### Basic Usage

```bash
# Add a task to the queue
python -m chapter_rewriter.cli add-task input.md

# Process all pending tasks
python -m chapter_rewriter.cli process-tasks
```

## 📚 Supported Input File Formats

- **Markdown**: `.md`
- **Text**: `.txt`

❌ **PDF**:  `.pdf` (not supported) use [MinerU](https://github.com/opendatalab/MinerU) to extract markdown from PDF

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

### Cleaning 

```bash
./clean.bat  # Windows User
./clean.sh  # Linux User
```




## 🔧 Configuration

### Environment Variables

- `API_KEY`: Your API key
- `BASE_URL`: API base URL (change for regional access)
- `MAX_TOKENS`: Restrict the length of model's response, default: 4096. Expand to 8192 if using Deepseek-R1.

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