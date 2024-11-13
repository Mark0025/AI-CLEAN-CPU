# Testing Guide for Directory Cleanup Application

## 🚀 Quick Start for Beginners

### Setting Up Your Test Environment

1. **Create a New Virtual Environment**
   ```bash
   # Navigate to your project directory
   cd directory-cleanup

   # Create a new virtual environment
   python -m venv test_env

   # Activate the virtual environment
   # On Windows:
   test_env\Scripts\activate
   # On macOS/Linux:
   source test_env/bin/activate
   ```

2. **Install Test Dependencies**
   ```bash
   # Install required packages
   pip install pytest pytest-asyncio pytest-cov pytest-mock colorama python-dotenv openai

   # Verify installation
   pytest --version
   ```

3. **Running Your First Test**
   ```bash
   # Run all tests
   pytest

   # Run tests with detailed output
   pytest -v

   # Run tests with coverage report
   pytest --cov=directory_cleanup

   # Run a specific test file
   pytest tests/test_analyzer.py

   # Run tests matching a specific name
   pytest -k "test_analyze"
   ```

4. **Understanding Test Output**
   - `.` means test passed
   - `F` means test failed
   - `E` means test had an error
   - `s` means test was skipped

5. **Common Issues and Solutions**
   - If `pytest` command not found: Make sure you're in your virtual environment
   - If imports failing: Check your PYTHONPATH
   - If tests failing: Read the error message carefully, it tells you exactly what went wrong

### Tips for Beginners
- Always run tests in a virtual environment
- Start with simple tests and build up
- Use `-v` flag to see more details
- Use `-s` flag to see print statements
- Keep test environment separate from development environment

## Overview of Testing Strategy

Our testing approach uses pytest for its simplicity and powerful features. Testing helps us:
1. Catch bugs early
2. Ensure code reliability
3. Enable safe refactoring
4. Document expected behavior
5. Speed up development

## Test Structure

### 1. Unit Tests (`test_analyzer.py`)
Tests the core functionality of the DirectoryAnalyzer class.

```python
class TestDirectoryAnalyzer:
    async def test_analyze_directories(self, analyzer, test_directory):
        all_dirs, stats = await analyzer.analyze_directories()
        assert stats["empty_directories"] == 3  # Verifies correct empty directory count
```

Key Features:
- Uses fixtures for test setup
- Mocks file system operations
- Tests error handling
- Verifies directory counting
- Checks cleanup operations

### 2. AI Safety Tests (`test_ai_safety.py`)
Tests the AI integration and safety checks.

```python
class TestAISafety:
    async def test_cached_responses(self, ai_safety, cache_manager, mock_openai):
        result1 = await ai_safety.validate_empty_directory(test_path)
        result2 = await ai_safety.validate_empty_directory(test_path)
        assert mock_openai.call_count == 1  # Verifies caching works
```

Key Features:
- Mocks OpenAI API calls
- Tests caching mechanism
- Validates safety checks
- Ensures consistent responses

### 3. Strategy Tests (`test_strategies.py`)
Tests different cleanup strategies.

```python
class TestMoveStrategy:
    async def test_move_with_structure(self, tmp_path, mock_ai_safety):
        source = tmp_path / "source" / "nested" / "empty"
        result = await strategy.handle_empty_directory(source)
        assert (target_dir / "nested" / "empty").exists()
```

Key Features:
- Tests move operations
- Tests delete operations
- Verifies directory structure
- Checks error handling

## Testing Best Practices

### 1. Use of Fixtures
```python
@pytest.fixture
def test_directory(tmp_path):
    """Creates a temporary directory structure for testing."""
    base_dir = tmp_path / "test_dirs"
    base_dir.mkdir()
    return base_dir
```
Benefits:
- Isolated test environment
- Automatic cleanup
- Reusable test data
- Consistent starting state

### 2. Mocking
```python
@pytest.fixture
def mock_openai():
    with patch("openai.ChatCompletion.acreate") as mock:
        mock.return_value.choices = [Mock(message=Mock(content="YES"))]
        yield mock
```
Benefits:
- Fast execution
- No API costs
- Predictable behavior
- Isolated testing

### 3. Parametrized Testing
```python
@pytest.mark.parametrize("error_path", ["permission_error", "os_error"])
async def test_error_handling(self, analyzer, test_directory, error_path):
    # Tests multiple error scenarios with one test
```
Benefits:
- Tests multiple scenarios
- Reduces code duplication
- Comprehensive coverage
- Clear test intentions

## Running Tests

### Basic Test Run
```bash
pytest tests/
```

### With Coverage
```bash
pytest tests/ -v --cov=directory_cleanup --cov-report=html
```

### Specific Tests
```bash
pytest tests/test_analyzer.py -k "test_analyze_directories"
```

## Test-Driven Development (TDD)

1. **Write Test First**
```python
def test_new_feature():
    result = analyze_special_directory("/path")
    assert result.is_valid
```

2. **Watch It Fail**
- Run the test
- Verify it fails as expected

3. **Implement Feature**
```python
def analyze_special_directory(path):
    # Implement the feature
    return ValidationResult(is_valid=True)
```

4. **Run Tests Again**
- Verify implementation works
- Check for regressions

## Performance Optimization

### 1. Profiling Tests
```bash
pytest tests/ --profile
```

### 2. Parallel Testing
```bash
pytest tests/ -n auto
```

## Common Testing Patterns

### 1. Setup/Teardown
```python
def setup_method(self):
    self.temp_files = []

def teardown_method(self):
    for file in self.temp_files:
        file.unlink()
```

### 2. Context Managers
```python
@contextmanager
def temporary_directory():
    dir_path = Path("temp_test_dir")
    dir_path.mkdir()
    try:
        yield dir_path
    finally:
        shutil.rmtree(dir_path)
```

## Testing Benefits for Development Speed

1. **Faster Debugging**
   - Precise error location
   - Reproducible issues
   - Isolated test cases

2. **Safer Refactoring**
   - Immediate feedback
   - Regression detection
   - Confidence in changes

3. **Better Design**
   - Modular code
   - Clear interfaces
   - Documented behavior

4. **Continuous Integration**
   - Automated testing
   - Early error detection
   - Consistent quality

## Conclusion

Testing is crucial for:
- Maintaining code quality
- Speeding up development
- Preventing regressions
- Documenting behavior
- Enabling collaboration

Remember:
- Write tests first
- Keep tests focused
- Use meaningful assertions
- Maintain test coverage
- Review test results 