# 📚 ScholarForge: AI-Powered Text Rewriter

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Contributors](https://img.shields.io/github/contributors/yourusername/scholarforge.svg)](https://github.com/yourusername/scholarforge/graphs/contributors)
[![Stars](https://img.shields.io/github/stars/yourusername/scholarforge.svg)](https://github.com/yourusername/scholarforge/stargazers)
[![Issues](https://img.shields.io/github/issues/yourusername/scholarforge.svg)](https://github.com/yourusername/scholarforge/issues)

<!-- <div align="center">
  <img src="https://raw.githubusercontent.com/yourusername/scholarforge/main/docs/images/logo.png" alt="ScholarForge Logo" width="200"/>
  <p><em>Transform your academic writing with AI-powered rewriting</em></p>
</div> -->

## 🚀 What is ScholarForge?

ScholarForge is a powerful command-line tool that helps students, researchers, and writers improve their text by using AI to rewrite content while preserving the original meaning. It's perfect for:

- 📝 Rewriting academic papers and essays
- 🔄 Improving the clarity and flow of your writing
- 📚 Processing large documents in manageable chunks
- 🌐 Supporting multiple AI providers through configurable endpoints

## ✨ Key Features

- **Task Management**: Queue-based system for handling multiple rewriting tasks
- **Smart Chunking**: Process large documents in manageable pieces
- **Memory Context**: Maintain consistency across chunks with configurable memory
- **Progress Tracking**: Real-time progress updates with detailed information
- **Flexible API Support**: Works with OpenAi API(DeepSeek, Qwen, etc.)
- **Resumable Processing**: Continue interrupted tasks without losing progress

## 🌍 Global Accessibility

ScholarForge is designed to work worldwide:

- **Multiple API Endpoints**: Configure different base URLs for regional access
- **Not in China?**: Use `https://api.siliconflow.cn/v1` for better connectivity

## 🛠️ Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/Monthlyaway/scholarforge.git
cd scholarforge

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

Edit the `.env` file with your API key and preferred settings:

```
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1  # Change to https://api.siliconflow.cn/v1 if needed
```

## 📖 Usage

### 📝 Input File Requirements

- ✅ Text-based files only (`.txt`, `.md`, etc.)
- ❌ PDF files not supported yet
- 💡 For PDF files, please convert to markdown first using [MinerU](https://github.com/opendatalab/MinerU), an open-source tool for extracting text from PDFs

### Basic Usage

```bash
# Add a task to the queue
python -m chapter_rewriter.cli add-task input.txt
python -m chapter_rewriter.cli add-task input.md

# Process all pending tasks
python -m chapter_rewriter.cli process-tasks
```

### Advanced Options

```bash
# Add a task with custom chunk size and memory context
python -m chapter_rewriter.cli add-task --chunk-size 2000 --memory-size 3 input.txt

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

ScholarForge is designed with students in mind:

- **Study Notes**: Rewrite your notes(or lecture notes, lecture slides, etc.) for better clarity and understanding
- **Research Papers**: Process and improve large academic documents
- **Language Learning**: See how AI rewrites text to improve your language skills
- **Essay Improvement**: Enhance your writing without changing the meaning

## 🔧 Configuration

### Environment Variables

- `DEEPSEEK_API_KEY`: Your API key
- `DEEPSEEK_BASE_URL`: API base URL (change for regional access)

### Task-Specific Settings

Each task can have its own settings stored in `task.json`:

- `chunk_size`: Size of text chunks to process
- `memory_size`: Number of previous chunks to include for context

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Thanks to all contributors who have helped improve ScholarForge
- Special thanks to the open-source community for inspiration and tools


---

<div align="center">
  <p>Made with ❤️ for students and writers worldwide</p>
</div> 