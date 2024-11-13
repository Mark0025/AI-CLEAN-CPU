"""Basic test suite for directory cleanup strategies."""

import pytest
from pathlib import Path
from strategies.move_strategy import MoveStrategy

def test_move_empty_directory(test_directory):
    """Test basic directory move functionality."""
    # Setup
    source_dir = test_directory / "source"
    source_dir.mkdir()
    target_dir = test_directory / "target"
    
    # Execute
    strategy = MoveStrategy(target_dir)
    strategy.execute(source_dir)
    
    # Verify
    assert not source_dir.exists()
    assert (target_dir / "source").exists() 