"""Basic pytest configuration."""

import pytest
from pathlib import Path

@pytest.fixture
def test_directory(tmp_path):
    """Create a simple test directory structure."""
    test_dir = tmp_path / "test_dirs"
    test_dir.mkdir()
    return test_dir