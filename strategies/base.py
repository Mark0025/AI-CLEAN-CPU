"""Base strategy for directory operations."""

from pathlib import Path
from abc import ABC, abstractmethod
import logging

class BaseStrategy(ABC):
    """Base class for directory operation strategies."""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def execute(self, source_dir: Path) -> bool:
        """Execute the strategy on the given directory."""
        pass