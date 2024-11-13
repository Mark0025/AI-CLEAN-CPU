#!/usr/bin/env python3
"""Test runner script."""

import pytest
import sys
import os
from pathlib import Path

def main():
    """Run the test suite."""
    # Add project root to Python path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # Run pytest
    args = [
        '-v',
        '--tb=short',
        'tests/',
    ]
    
    # Add coverage if requested
    if '--coverage' in sys.argv:
        args.extend([
            '--cov=directory_cleanup',
            '--cov-report=html',
            '--cov-report=term-missing'
        ])
    
    exit_code = pytest.main(args)
    sys.exit(exit_code)

if __name__ == '__main__':
    main() 