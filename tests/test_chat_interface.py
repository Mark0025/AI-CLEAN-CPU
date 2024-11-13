"""Test suite for chat interface commands."""

import pytest
from pathlib import Path
import tempfile
import os
import shutil
from core.chat_interface import CleanupAssistant

class TestCleanupAssistant:
    """Test class for CleanupAssistant."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.assistant = CleanupAssistant()
        
        # Create test files and directories
        (Path(self.test_dir) / "empty_file.txt").touch()
        (Path(self.test_dir) / "test.txt").write_text("content")
        (Path(self.test_dir) / "empty_dir").mkdir()
        
        nonempty_dir = Path(self.test_dir) / "nonempty_dir"
        nonempty_dir.mkdir()
        (nonempty_dir / "file.txt").write_text("content")
        
        yield
        
        # Cleanup
        shutil.rmtree(self.test_dir)
    
    def test_basic_commands(self):
        """Test basic navigation and information commands."""
        # Test help
        response = self.assistant.handle_command("help")
        assert "Available Commands" in response or "commands" in response.lower()
        
        # Test ls
        response = self.assistant.handle_command("ls")
        assert "Current directory contents" in response
        
        # Test directory navigation
        response = self.assistant.handle_command("cd ..")
        assert "Changed directory to" in response

    def test_empty_file_detection(self):
        """Test empty file detection and handling."""
        # Change to test directory
        self.assistant.handle_command(f"cd {self.test_dir}")
        
        # Test finding empty files using our internal method
        response = self.assistant.handle_command("show me empty files")
        assert "empty_file.txt" in response

    def test_empty_directory_detection(self):
        """Test empty directory detection and handling."""
        self.assistant.handle_command(f"cd {self.test_dir}")
        
        response = self.assistant.handle_command("show me empty directories")
        assert "empty_dir" in response

    def test_natural_language_commands(self):
        """Test natural language command processing."""
        # Change to test directory first
        self.assistant.handle_command(f"cd {self.test_dir}")
        
        test_cases = [
            ("what's in this directory", lambda r: "Current directory contents" in r and "empty_file.txt" in r),
            ("show me empty files", lambda r: "Found empty files" in r and "empty_file.txt" in r),
            ("show directory contents", lambda r: "Current directory contents" in r and "empty_file.txt" in r),
            ("go to ..", lambda r: "Changed directory to" in r)
        ]
        
        for cmd, validator in test_cases:
            response = self.assistant.handle_command(cmd)
            assert response is not None, f"No response for command: {cmd}"
            assert validator(response), f"Command '{cmd}' failed validation.\nResponse: {response}"
            assert not any(err in response.lower() for err in ["error:", "failed:", "could not"])

    def test_system_commands(self):
        """Test system command execution."""
        # Test direct command with printf instead of echo
        response = self.assistant.handle_command("!printf 'test'")
        assert "test" in response
        
        # Test pwd
        response = self.assistant.handle_command("!pwd")
        assert str(self.assistant.current_path) in response

    def test_error_handling(self):
        """Test error handling for invalid commands and operations."""
        # Test invalid directory
        response = self.assistant.handle_command("cd /nonexistent/path")
        assert "Error" in response or "not exist" in response
        
        # Test invalid command
        response = self.assistant.handle_command("invalid_command")
        assert "Not sure what you want to do" in response

    def test_special_paths(self):
        """Test handling of special paths and shortcuts."""
        # Test home directory
        response = self.assistant.handle_command("home")
        assert str(Path.home()).lower() in response.lower()
        
        # Test desktop navigation
        response = self.assistant.handle_command("desktop")
        # More flexible check for desktop path
        desktop_path = str(Path.home() / "Desktop").lower()
        assert desktop_path in response.lower()
  