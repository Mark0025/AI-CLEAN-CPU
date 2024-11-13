"""Logging configuration and utilities."""

import logging
from pathlib import Path
from datetime import datetime

def setup_logging(log_dir: str = "logs") -> str:
    """Configure logging with timestamp-based log file."""
    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(exist_ok=True, parents=True)
    
    # Create timestamped log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_dir}/cleanup_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return log_file 