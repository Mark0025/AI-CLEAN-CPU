"""Basic strategy for moving directories."""

import logging
from pathlib import Path
import shutil

class MoveStrategy:
    def __init__(self, target_dir: Path):
        self.target_dir = Path(target_dir)
        self.logger = logging.getLogger(__name__)
        
    def execute(self, source_dir: Path) -> None:
        """Move directory to target location."""
        try:
            # Ensure target directory exists
            self.target_dir.mkdir(parents=True, exist_ok=True)
            
            # Simple move operation
            shutil.move(str(source_dir), str(self.target_dir))
            self.logger.info(f"Moved {source_dir} to {self.target_dir}")
            
        except Exception as e:
            self.logger.error(f"Failed to move {source_dir}: {e}")
            raise