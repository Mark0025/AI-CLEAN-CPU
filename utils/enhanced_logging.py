"""Enhanced logging system with structured logging and AI interaction tracking."""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from functools import wraps
import time
import traceback

class EnhancedLogger:
    """Enhanced logging with structured output and performance tracking."""
    
    def __init__(self, log_dir: str = "logs"):
        self.base_dir = Path(log_dir)
        self.setup_log_directories()
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def setup_log_directories(self) -> None:
        """Create structured log directories."""
        (self.base_dir / "ai_interactions").mkdir(parents=True, exist_ok=True)
        (self.base_dir / "operations").mkdir(parents=True, exist_ok=True)
        (self.base_dir / "errors").mkdir(parents=True, exist_ok=True)
        (self.base_dir / "performance").mkdir(parents=True, exist_ok=True)
    
    def log_ai_interaction(self, interaction_type: str, prompt: str, response: str, 
                          metadata: Optional[Dict] = None) -> None:
        """Log AI interactions with context."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': interaction_type,
            'prompt': prompt,
            'response': response,
            'metadata': metadata or {},
            'session_id': self.session_id
        }
        
        file_path = self.base_dir / "ai_interactions" / f"ai_log_{self.session_id}.jsonl"
        with file_path.open('a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def log_operation(self, operation_type: str, details: Dict[str, Any], 
                     status: str = "success") -> None:
        """Log directory operations with details."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation_type,
            'status': status,
            'details': details,
            'session_id': self.session_id
        }
        
        file_path = self.base_dir / "operations" / f"op_log_{self.session_id}.jsonl"
        with file_path.open('a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def log_error(self, error: Exception, context: Dict[str, Any]) -> None:
        """Log detailed error information."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'error_type': error.__class__.__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context,
            'session_id': self.session_id
        }
        
        file_path = self.base_dir / "errors" / f"error_log_{self.session_id}.jsonl"
        with file_path.open('a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def performance_decorator(self, operation_name: str):
        """Decorator to track operation performance."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    duration = time.time() - start_time
                    
                    # Log performance metrics
                    metrics = {
                        'operation': operation_name,
                        'duration': duration,
                        'success': True,
                        'timestamp': datetime.now().isoformat(),
                        'session_id': self.session_id
                    }
                    
                    file_path = self.base_dir / "performance" / f"perf_log_{self.session_id}.jsonl"
                    with file_path.open('a') as f:
                        f.write(json.dumps(metrics) + '\n')
                    
                    return result
                    
                except Exception as e:
                    duration = time.time() - start_time
                    # Log failure metrics
                    metrics = {
                        'operation': operation_name,
                        'duration': duration,
                        'success': False,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat(),
                        'session_id': self.session_id
                    }
                    
                    file_path = self.base_dir / "performance" / f"perf_log_{self.session_id}.jsonl"
                    with file_path.open('a') as f:
                        f.write(json.dumps(metrics) + '\n')
                    
                    raise
                    
            return wrapper
        return decorator

# Create global logger instance
enhanced_logger = EnhancedLogger()

# Example usage:
# @enhanced_logger.performance_decorator("analyze_directory")
# def analyze_directory():
#     pass 