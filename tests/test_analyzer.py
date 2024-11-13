"""Test suite for DirectoryAnalyzer class."""

import pytest
import os
from pathlib import Path
import shutil
from unittest.mock import Mock, patch
from datetime import datetime

from core.analyzer import DirectoryAnalyzer
from utils.progress import ProgressTracker
from strategies.move_strategy import MoveStrategy
from utils.ai_safety import AISafetyCheck

@pytest.fixture
def test_directory(tmp_path):
    """Create a temporary directory structure for testing."""
    # Create test directory structure
    base_dir = tmp_path / "test_dirs"
    base_dir.mkdir()
    
    # Create some empty directories
    (base_dir / "empty1").mkdir()
    (base_dir / "empty2").mkdir()
    
    # Create non-empty directories
    nonempty = base_dir / "nonempty"
    nonempty.mkdir()
    (nonempty / "file.txt").write_text("content")
    
    # Create nested structure
    nested = base_dir / "nested"
    nested.mkdir()
    (nested / "empty_nested").mkdir()
    
    return base_dir

@pytest.fixture
def mock_ai_safety():
    """Create a mock AI safety checker."""
    mock = Mock(spec=AISafetyCheck)
    mock.validate_empty_directory.return_value = True
    return mock

@pytest.fixture
def analyzer(test_directory, mock_ai_safety):
    """Create DirectoryAnalyzer instance with test configuration."""
    strategy = MoveStrategy(str(test_directory / "moved_dirs"), mock_ai_safety)
    return DirectoryAnalyzer(
        start_dir=str(test_directory),
        strategy=strategy,
        progress_tracker=ProgressTracker(),
    )

class TestDirectoryAnalyzer:
    """Test cases for DirectoryAnalyzer."""
    
    async def test_analyze_directories(self, analyzer, test_directory):
        """Test directory analysis functionality."""
        all_dirs, stats = await analyzer.analyze_directories()
        
        assert all_dirs is not None
        assert len(all_dirs) > 0
        assert stats["empty_directories"] == 3  # empty1, empty2, empty_nested
        
    async def test_execute_cleanup(self, analyzer, test_directory):
        """Test cleanup execution."""
        # First analyze
        await analyzer.analyze_directories()
        
        # Then execute cleanup
        result = await analyzer.execute_cleanup()
        assert result is True
        
        # Check if empty directories were processed
        moved_dirs = list(Path(analyzer.strategy.target_dir).glob("**/*"))
        assert len(moved_dirs) == 3
    
    async def test_skip_nonempty_directories(self, analyzer, test_directory):
        """Test that non-empty directories are skipped."""
        await analyzer.analyze_directories()
        await analyzer.execute_cleanup()
        
        # Check that non-empty directory still exists
        nonempty = test_directory / "nonempty"
        assert nonempty.exists()
        assert (nonempty / "file.txt").exists()
    
    @pytest.mark.parametrize("error_path", ["permission_error", "os_error"])
    async def test_error_handling(self, analyzer, test_directory, error_path, caplog):
        """Test error handling during analysis and cleanup."""
        error_dir = test_directory / error_path
        error_dir.mkdir()
        
        if error_path == "permission_error":
            error = PermissionError("Access denied")
        else:
            error = OSError("Generic error")
        
        with patch("pathlib.Path.iterdir", side_effect=error):
            all_dirs, stats = await analyzer.analyze_directories()
            
        assert "Error accessing" in caplog.text
        assert stats["errors"] > 0 