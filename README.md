# SlopAuthor


## Note: ** Experiment in progress. Haven't decided where I want to take this project eventually. Stable but may introduce breaking changes and altered features with future commits. Use at your own discretion **

An autonomous AI writing agent powered by Google's Gemini 3 Flash — built to explore the limits of 1M token context windows and flash thinking capabilities.

## The Experiment

This project started as an experiment: **What happens when you give an AI agent autonomy, a massive context window, and let it write complete novels?**

Inspired by Claude Code's agentic approach, I wanted to build a CLI-only writing agent that could:
- Plan and execute complex creative writing tasks independently  
- Leverage Gemini's 1M token context for truly long-form content
- Use flash thinking for better reasoning about narrative structure

I received $300 in Google AI credits and decided to put them to good use — building an agent that doesn't just assist with writing, but actually *writes*.

## What It Does

```
You: "Write a 10-chapter mystery novel set in Victorian London"

Agent: *thinks* → *creates project* → *plans structure* → *writes 50,000+ words* → Done.
```

The agent autonomously:
- 📁 Creates organized project structures
- 📝 Writes complete, publication-ready content (3,000-10,000 words per file)
- 🔄 Manages its own context with smart compression
- 💾 Auto-saves progress and supports recovery from interruptions
- 📚 Supports templates for novels, short stories, technical books, and screenplays

## Quick Start

### Prerequisites

- Python 3.10+
- [Gemini API Key](https://aistudio.google.com/app/apikey)

### Installation

```bash
# Clone the repository
git clone https://github.com/NahinNilav/slopauthor.git
cd slopauthor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp env.example .env
# Edit .env and add your GEMINI_API_KEY
```
## CLI Reference

### Basic Commands

#### Get Help
```bash
python main.py --help
# Shows all available options and usage examples
```

#### List Templates
```bash
python main.py --list-templates
# or
python main.py -l
```
Displays all available project templates with descriptions.

#### Interactive Mode
```bash
python main.py
```
Starts interactive prompt where you can enter your writing request.

### Writing Commands

#### Simple Prompt
```bash
python main.py "Your writing request here"
```
**Examples:**
```bash
python main.py "Write 5 sci-fi short stories about AI consciousness"
python main.py "Create a mystery novel with 10 chapters"
python main.py "Write a beginner's guide to Python with 15 chapters"
```

#### With Template
```bash
python main.py --template <template_name> "Your writing request"
# or
python main.py -t <template_name> "Your writing request"
```
**Examples:**
```bash
# Novel with structure
python main.py --template novel "Write a thriller set in Tokyo"

# Short story collection
python main.py -t short_stories "5 interconnected stories about time travel"

# Technical book
python main.py --template technical_book "Complete guide to Docker and containers"

# Screenplay
python main.py -t screenplay "Action thriller screenplay - 90 pages"
```

### Recovery & Resumption

#### Resume From Checkpoint
```bash
python main.py --recover <path_to_summary_file>
```
**Example:**
```bash
python main.py --recover output/my_novel/.context_summary_20260103_143022.md
```

When to use:
- Agent was interrupted (Ctrl+C)
- Hit the 300 iteration limit
- Want to continue/expand previous work
- Found in your project folder as `.context_summary_YYYYMMDD_HHMMSS.md`

### Command Options Summary

| Option | Short | Description |
|--------|-------|-------------|
| `--help` | `-h` | Show help message |
| `--template` | `-t` | Use a project template |
| `--list-templates` | `-l` | List all templates |
| `--recover` | - | Resume from saved checkpoint |

### Output Location

All generated content is saved in:
```
output/<project_name>/
├── README.md              # Project overview
├── chapter_01.md          # Generated content
├── chapter_02.md
├── ...
└── .context_summary_*.md  # Auto-saved checkpoints
```

### Tips

**💡 Be Specific:** Clear prompts get better results
- ✅ "Write a 10-chapter mystery novel set in Victorian London with a detective protagonist"
- ❌ "Write something interesting"

**💡 Let It Work:** The agent is autonomous - it will plan and execute the full task without intervention

**💡 Use Templates:** Templates provide structure and save the agent from reinventing the wheel

**💡 Monitor Progress:** Check the `output/<project_name>/` folder to see files being created in real-time

**💡 Recovery is Easy:** Press Ctrl+C to interrupt, then use `--recover` with the latest `.context_summary_*.md` file

## Templates

| Template | Description |
|----------|-------------|
| `novel` | Full novel structure with chapters, character bible, worldbuilding |
| `short_stories` | Collection format with author notes |
| `technical_book` | Educational content with exercises and glossary |
| `screenplay` | Film/TV format with beat sheets and treatments |

## How It Works

1. **Agentic Loop**: The agent runs up to 300 iterations, each time reasoning about what to do next
2. **Tool Use**: It can create projects, write files, and manage context
3. **Context Management**: Auto-compresses at 900K tokens to stay within limits
4. **Recovery**: Interrupted? Resume from any saved checkpoint
---

*Built with curiosity and $300 in API credits.*

