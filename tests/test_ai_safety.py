"""Test suite for AI safety features."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path

from utils.ai_safety import AISafetyCheck
from utils.cache_manager import CacheManager

@pytest.fixture
def mock_openai():
    """Mock OpenAI API responses."""
    with patch("openai.ChatCompletion.acreate") as mock:
        mock.return_value = AsyncMock()
        mock.return_value.choices = [
            Mock(message=Mock(content="YES - This directory appears safe to process."))
        ]
        yield mock

@pytest.fixture
def ai_safety(mock_openai):
    """Create AISafetyCheck instance with mocked OpenAI."""
    with patch("utils.ai_safety.AISafetyCheck.get_final_confirmation", 
              new_callable=AsyncMock, return_value=True):
        return AISafetyCheck()

@pytest.fixture
def cache_manager(tmp_path):
    """Create CacheManager with temporary directory."""
    return CacheManager(cache_dir=str(tmp_path / "cache"))

class TestAISafety:
    """Test cases for AI safety features."""
    
    async def test_directory_recommendation(self, ai_safety, mock_openai):
        """Test getting directory recommendations."""
        location = "/test/path"
        is_safe = await ai_safety.get_directory_recommendation()
        
        assert mock_openai.called
        assert isinstance(is_safe, bool)
    
    async def test_validate_empty_directory(self, ai_safety, mock_openai):
        """Test directory validation."""
        test_path = Path("/test/empty/dir")
        is_safe = await ai_safety.validate_empty_directory(test_path)
        
        assert mock_openai.called
        assert isinstance(is_safe, bool)
    
    async def test_cached_responses(self, ai_safety, cache_manager, mock_openai):
        """Test that responses are properly cached."""
        test_path = Path("/test/cache/dir")
        
        # First call should use API
        result1 = await ai_safety.validate_empty_directory(test_path)
        assert mock_openai.call_count == 1
        
        # Second call should use cache
        result2 = await ai_safety.validate_empty_directory(test_path)
        assert mock_openai.call_count == 1  # No additional API calls
        assert result1 == result2 