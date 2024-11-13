# 🧠 AI-CLEAN-CPU

> Your Intelligent File System Guardian: AI-Powered Cleanup and Organization

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![OpenAI](https://img.shields.io/badge/AI-OpenAI%20GPT--4-brightgreen.svg)](https://openai.com/)

## 🌟 Overview

AI-CLEAN-CPU revolutionizes file system management by combining artificial intelligence with robust system operations. This intelligent tool not only cleans and organizes your files but understands context, preserves important data, and learns from your preferences.

## ✨ Key Features

### 🤖 AI-Powered Intelligence
- **Natural Language Interface**: Talk to your file system naturally
- **Context-Aware Operations**: AI understands directory purposes and relationships
- **Smart Risk Assessment**: Prevents accidental deletion of critical files
- **Learning Capabilities**: Adapts to your organization preferences

### 🛡️ Advanced Safety Systems
- **Multi-Layer Validation**: Triple-check safety protocol
- **Rollback Capability**: All operations can be undone
- **Transaction-Based Operations**: Atomic operations prevent partial changes
- **Intelligent Backup**: Automated backup before risky operations

### 📊 Smart Analytics
- **Directory Pattern Recognition**: Identifies organization patterns
- **Usage Analysis**: Tracks file access and modification patterns
- **Space Optimization**: Identifies redundant and unnecessary files
- **Impact Prediction**: Estimates cleanup impact before execution

### ⚡ Performance Features
- **Async Operations**: Non-blocking file system operations
- **Intelligent Caching**: Caches frequent operations and AI responses
- **Batch Processing**: Optimized bulk operations
- **Resource Management**: Adaptive resource utilization

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key
- 500MB free disk space

### Quick Install
1. Clone the repository:
```bash
git clone https://github.com/Mark0025/AI-CLEAN-CPU.git
```

## 📚 Usage Guide

### Basic Commands
```bash
# Start the application
python main.py

# Start with specific directory
python main.py /path/to/directory

# Start in analysis-only mode
python main.py --analyze
```

### 🎯 Command Examples

1. **Navigation Commands**
```bash
> cd Downloads          # Change to Downloads directory
> ls                    # List current directory contents
> back                  # Go back to previous directory
> home                  # Return to home directory
```

2. **Cleanup Commands**
```bash
> clean                 # Start interactive cleanup
> analyze              # Analyze current directory
> show empty           # Show empty files and directories
> delete empty         # Safely remove empty items
> organize             # Auto-organize current directory
```

3. **Search Commands**
```bash
> find large           # Find large files
> search "*.txt"       # Search for text files
> find duplicates      # Find duplicate files
> show recent          # Show recently modified files
```

4. **Safety Commands**
```bash
> backup              # Create backup of current directory
> restore             # Restore from last backup
> undo                # Undo last operation
> status              # Show operation status
```

### 💡 Natural Language Examples
The assistant understands natural language commands like:

```bash
> "Clean up my downloads folder"
> "Find all empty directories"
> "Move large files to external drive"
> "Show me what files I haven't used in 6 months"
> "Organize my photos by date"
```

### 🛡️ Safety Features in Action

1. **Before Any Operation**
```bash
> delete empty
📊 Analysis Summary:
- Empty files found: 5
- Empty directories found: 3
⚠️ Safety Check: All items verified as safe to remove
? Proceed with deletion? [Y/n]:
```

2. **Backup Creation**
```bash
> organize
📂 Creating backup...
✅ Backup created: backup_20240124_153022
🔍 Analyzing directory structure...
```

3. **Operation Confirmation**
```bash
> clean
🔍 Found 25 items to clean
📊 Impact Analysis:
  - Space to be freed: 2.5GB
  - Files to be moved: 15
  - Files to be deleted: 10
? Review changes? [Y/n]:
```

### ⚙️ Configuration Tips

1. **Set Default Behavior**
Edit your `.env` file to customize:
```bash
# Enable automatic backups
BACKUP_ENABLED=true

# Set safety level
SAFE_MODE=true
REQUIRE_CONFIRMATION=true

# Configure cleanup preferences
AUTO_CLEANUP=false
DRY_RUN=true
```

2. **Customize Exclusions**
```bash
# In .env file
EXCLUDED_DIRS=node_modules,venv,.git
EXCLUDED_FILES=.env,.DS_Store,Thumbs.db
```

### 🚨 Error Handling

The application provides clear error messages and recovery options:
```bash
> delete important_file.txt
❌ Error: Operation blocked by safety check
ℹ️ Reason: File appears to be important
💡 Suggestion: Use 'force' flag to override or 'analyze' for details
```

### 📊 Getting Help

```bash
> help                  # Show all available commands
> help clean           # Show help for clean command
> examples             # Show usage examples
> status              # Show system status
```

For more detailed documentation, see our [User Guide](docs/user-guide.md).
