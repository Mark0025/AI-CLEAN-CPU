# Directory Cleanup Utility with AI Safety

A Python-based utility for efficiently managing empty directories with AI-powered safety checks. This tool helps you identify and manage empty directories while using OpenAI's GPT to prevent accidental deletion of important system files.

## 🌟 Features

- 🤖 AI-powered safety validation
- 🔍 Efficient directory scanning and analysis
- 📊 Real-time progress tracking
- 📝 Comprehensive logging
- 🔄 Multiple cleanup strategies (move or delete)
- ⚡ Asynchronous operations
- 🛡️ Multi-layer safety checks
- 📁 Directory structure preservation

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/markcarpenter0025/directory-cleanup.git
cd directory-cleanup
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up OpenAI API key:
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 🎯 Usage

Run the application:
```bash
python main.py [directory_path]
```

The application will:
1. Ask about your cleanup intentions
2. Perform AI safety analysis of the target directory
3. Provide recommendations and warnings
4. Execute the chosen strategy with continuous safety checks

### 🔒 Safety Features

1. **AI-Powered Validation**
   - Analyzes directory context and purpose
   - Identifies potential system directories
   - Prevents accidental deletion of important files
   - Provides detailed safety recommendations

2. **Multiple Safety Layers**
   - Initial directory assessment
   - Per-directory validation
   - Final confirmation for deletions
   - Comprehensive logging of decisions

### 🔄 Cleanup Strategies

1. **Move Strategy (Default)**
   - Safely relocates empty directories
   - Maintains original structure
   - Allows easy recovery if needed
   - AI validation before each move

2. **Delete Strategy**
   - Permanent removal option
   - Double AI safety check
   - Requires explicit confirmation
   - Detailed logging of deletions

## 📁 Project Structure

```
directory_cleanup/
├── core/
│   ├── analyzer.py      # Main analysis logic
│   └── constants.py     # Configuration
├── utils/
│   ├── ai_safety.py     # AI safety checks
│   ├── logging_utils.py # Logging setup
│   └── progress.py      # Progress tracking
├── strategies/
│   ├── base.py         # Strategy interface
│   ├── move_strategy.py # Move implementation
│   └── delete_strategy.py # Delete implementation
└── main.py             # Entry point
```

## 📊 Logging and Monitoring

- **Detailed Logs**
  - Operation timestamps
  - AI safety recommendations
  - Directory processing status
  - Error tracking

- **Progress Tracking**
  - Real-time progress updates
  - Directory counts and statistics
  - Time estimates
  - Operation summaries

## ⚙️ Configuration

Customize skip directories in `core/constants.py`:
```python
SKIP_DIRS = {
    '.git',
    'node_modules',
    '__pycache__',
    # Add custom directories
}
```

## 🛡️ Safety Best Practices

1. **Before Running**
   - Review AI safety recommendations
   - Use move strategy for initial testing
   - Backup important data
   - Check skip directories list

2. **During Operation**
   - Monitor progress and logs
   - Watch for AI warnings
   - Don't interrupt long operations
   - Check error messages

3. **After Completion**
   - Review operation logs
   - Verify moved/deleted directories
   - Check for error reports
   - Maintain backup logs

## 🔧 Performance Tips

1. **Large Directory Structures**
   - Use move strategy initially
   - Run during low-activity periods
   - Monitor system resources
   - Consider batch processing

2. **Network Directories**
   - Account for latency
   - Check permissions
   - Use appropriate timeouts
   - Monitor network stability

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔍 Troubleshooting

- Check the log files for detailed error messages
- Verify OpenAI API key is correctly set
- Ensure proper directory permissions
- Monitor system resource usage

## 📚 Documentation

For detailed documentation of each module and feature, see the `docs/` directory.

## 🙏 Acknowledgments

- OpenAI for providing the GPT API
- Python community for essential libraries
- Contributors and testers

## 📧 Support

For support, please:
1. Check existing issues
2. Review documentation
3. Create a detailed issue
4. Join our community discussions# AI-CLEAN-CPU
