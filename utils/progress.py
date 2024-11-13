"""Progress tracking utilities."""

import logging
from datetime import datetime

class ProgressTracker:
    """Track progress of directory operations."""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.logger = logging.getLogger(__name__)
        self.total_processed = 0
        
    def update(self, current: int, total: int):
        """Update progress."""
        self.total_processed = current
        if total > 0:
            percentage = (current / total) * 100
            self.logger.info(f"Progress: {current}/{total} ({percentage:.1f}%)") 