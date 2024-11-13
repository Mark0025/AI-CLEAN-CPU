"""Test suite for checking application readiness."""

import pytest
import os
from pathlib import Path
import importlib
import sys

def test_required_files_exist():
    """Verify all required files are present."""
    base_dir = Path(__file__).parent.parent  # Go up one directory from tests
    required_files = [
        'class.py',  # We have this one
        'core/analyzer.py',
        'core/constants.py',
        'utils/ai_safety.py',
        'utils/logging_utils.py',
        'utils/progress.py',
        'strategies/base.py',
        'strategies/move_strategy.py',
        'strategies/delete_strategy.py',
        '.env'
    ]
    
    missing_files = []
    for file in required_files:
        if not (base_dir / file).exists():
            missing_files.append(file)
    
    assert not missing_files, f"Missing required files: {missing_files}"

def test_environment_setup():
    """Check environment configuration."""
    assert 'OPENAI_API_KEY' in os.environ or Path('.env').exists(), \
        "OpenAI API key not configured"

def test_dependencies_installed():
    """Verify all required dependencies are installed."""
    required_packages = [
        'openai',
        'python-dotenv',
        'colorama',
        'pytest',
        'pytest-asyncio',
        'pytest-cov'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            missing_packages.append(package)
    
    assert not missing_packages, f"Missing required packages: {missing_packages}" 