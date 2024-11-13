"""Configure test environment."""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent)
sys.path.insert(0, project_root) 