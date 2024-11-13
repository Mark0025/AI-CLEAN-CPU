"""Constants used throughout the application."""

from pathlib import Path

# Directories to skip during cleanup
SKIP_DIRS = {
    '.git',
    'venv',
    'node_modules',
    '__pycache__'
}

# Default paths
DEFAULT_LOG_DIR = Path('logs')
DEFAULT_CONFIG_DIR = Path('config') 