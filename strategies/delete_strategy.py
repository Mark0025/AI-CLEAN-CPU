"""Strategy for deleting empty directories."""

import logging
from pathlib import Path
import shutil

from .base import DirectoryStrategy
from utils.ai_safety import AISafetyCheck

class DeleteStrategy(DirectoryStrategy):
    """Strategy that permanently deletes empty directories."""
    
    def __init__(self, ai_safety: AISafetyCheck):
        super().__init__(ai_safety)
        logging.warning("Delete strategy initialized - directories will be permanently removed")
    
    async def handle_empty_directory(self, dir_path: Path) -> bool:
        """Delete an empty directory."""
        if not await self.validate_directory(dir_path):
            return False
            
        try:
            # Double-check with AI before deletion
            confirmation_prompt = f"About to delete directory: {dir_path}\nConfirm this is safe?"
            if not await self.ai_safety.get_final_confirmation(dir_path):
                logging.warning(f"Deletion aborted by AI safety check: {dir_path}")
                self.skipped_count += 1
                return False
            
            shutil.rmtree(dir_path)
            self.processed_count += 1
            logging.info(f"Deleted empty directory: {dir_path}")
            return True
            
        except (OSError, shutil.Error) as e:
            logging.error(f"Failed to delete directory {dir_path}: {e}")
            return False
    
    def cleanup(self) -> None:
        """Log final deletion statistics."""
        logging.info(f"Delete Strategy Summary:")
        logging.info(f"- Directories deleted: {self.processed_count}")
        logging.info(f"- Directories skipped (AI safety): {self.skipped_count}")
        if self.processed_count > 0:
            logging.warning(f"Permanently deleted {self.processed_count} directories") 