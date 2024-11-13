"""Cache management for AI responses and directory analysis."""

import json
import hashlib
import time
from pathlib import Path
from typing import Any, Optional, Dict
from datetime import datetime, timedelta

class CacheManager:
    """Manages caching of AI responses and directory analysis results."""
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_base = Path(cache_dir)
        self.ai_cache = self.cache_base / "ai_responses"
        self.dir_cache = self.cache_base / "directory_stats"
        self._init_cache_dirs()
    
    def _init_cache_dirs(self) -> None:
        """Initialize cache directory structure."""
        self.ai_cache.mkdir(parents=True, exist_ok=True)
        self.dir_cache.mkdir(parents=True, exist_ok=True)
    
    def _generate_key(self, data: str) -> str:
        """Generate a cache key from input data."""
        return hashlib.md5(data.encode()).hexdigest()
    
    def get_ai_response(self, prompt: str, max_age: timedelta = timedelta(hours=24)) -> Optional[str]:
        """Retrieve cached AI response if available and not expired."""
        key = self._generate_key(prompt)
        cache_file = self.ai_cache / f"{key}.json"
        
        if cache_file.exists():
            with cache_file.open('r') as f:
                cached = json.load(f)
                
            if datetime.fromisoformat(cached['timestamp']) + max_age > datetime.now():
                return cached['response']
        
        return None
    
    def cache_ai_response(self, prompt: str, response: str) -> None:
        """Cache an AI response with timestamp."""
        key = self._generate_key(prompt)
        cache_file = self.ai_cache / f"{key}.json"
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt,
            'response': response
        }
        
        with cache_file.open('w') as f:
            json.dump(data, f, indent=2)
    
    def get_directory_stats(self, dir_path: str, max_age: timedelta = timedelta(hours=1)) -> Optional[Dict]:
        """Retrieve cached directory statistics if available and not expired."""
        key = self._generate_key(dir_path)
        cache_file = self.dir_cache / f"{key}.json"
        
        if cache_file.exists():
            with cache_file.open('r') as f:
                cached = json.load(f)
                
            if datetime.fromisoformat(cached['timestamp']) + max_age > datetime.now():
                return cached['stats']
        
        return None
    
    def cache_directory_stats(self, dir_path: str, stats: Dict) -> None:
        """Cache directory statistics with timestamp."""
        key = self._generate_key(dir_path)
        cache_file = self.dir_cache / f"{key}.json"
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'path': dir_path,
            'stats': stats
        }
        
        with cache_file.open('w') as f:
            json.dump(data, f, indent=2)
    
    def clear_expired_cache(self, max_age: timedelta = timedelta(days=7)) -> None:
        """Clear expired cache entries."""
        now = datetime.now()
        
        for cache_dir in [self.ai_cache, self.dir_cache]:
            for cache_file in cache_dir.glob('*.json'):
                with cache_file.open('r') as f:
                    cached = json.load(f)
                
                if datetime.fromisoformat(cached['timestamp']) + max_age < now:
                    cache_file.unlink() 