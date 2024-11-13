"""Directory analysis functionality."""

import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

from core.constants import SKIP_DIRS
from strategies.base import DirectoryStrategy
from utils.progress import ProgressTracker

class DirectoryAnalyzer:
    """Analyzes and processes directories."""
    
    def __init__(
        self,
        start_dir: str,
        strategy: DirectoryStrategy,
        progress_tracker: Optional[ProgressTracker] = None,
        skip_dirs: set = SKIP_DIRS
    ):
        self.start_dir = Path(start_dir)
        self.strategy = strategy
        self.progress = progress_tracker
        self.skip_dirs = skip_dirs
        self.logger = logging.getLogger(__name__)
        
    def analyze_directories(self) -> Tuple[List[str], Dict]:
        """Analyze directories and collect statistics."""
        try:
            if not self.start_dir.exists():
                self.logger.error(f"Start directory does not exist: {self.start_dir}")
                return None, {}
                
            stats = {
                "total_directories": 0,
                "empty_directories": 0,
                "errors": 0,
                "start_time": datetime.now().isoformat()
            }
            
            all_dirs = []
            
            for item in self.start_dir.rglob("*"):
                if item.is_dir() and not self._should_skip(item):
                    stats["total_directories"] += 1
                    if not any(item.iterdir()):
                        stats["empty_directories"] += 1
                        all_dirs.append(str(item))
                        
            return all_dirs, stats
            
        except Exception as e:
            self.logger.error(f"Error analyzing directories: {e}")
            return None, {}
    
    def _should_skip(self, path: Path) -> bool:
        """Check if directory should be skipped."""
        return any(skip_dir in path.parts for skip_dir in self.skip_dirs)
    
    def execute_cleanup(self) -> bool:
        """Execute the cleanup strategy."""
        try:
            all_dirs, _ = self.analyze_directories()
            if not all_dirs:
                return False
                
            for dir_path in all_dirs:
                try:
                    self.strategy.execute(Path(dir_path))
                except Exception as e:
                    self.logger.error(f"Error processing directory {dir_path}: {e}")
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
            return False 