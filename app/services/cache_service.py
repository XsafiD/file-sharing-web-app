"""
Cache Service - In-memory caching for file list
Reduces file system I/O for better performance
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path


class CacheService:
    """
    In-memory cache service with TTL support
    Can be extended to use Redis for distributed caching
    """

    def __init__(self, ttl_seconds: int = 5):
        """
        Initialize cache service

        Args:
            ttl_seconds: Time-to-live for cached data (default: 5 seconds)
        """
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Dict] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[List[Dict]]:
        """
        Get cached data if valid

        Args:
            key: Cache key

        Returns:
            Cached data or None if expired/not found
        """
        async with self._lock:
            if key not in self._cache:
                return None

            cached = self._cache[key]

            # Check if expired
            if datetime.now() > cached['expires_at']:
                del self._cache[key]
                return None

            return cached['data']

    async def set(self, key: str, data: List[Dict]) -> None:
        """
        Set data in cache with TTL

        Args:
            key: Cache key
            data: Data to cache
        """
        async with self._lock:
            self._cache[key] = {
                'data': data,
                'created_at': datetime.now(),
                'expires_at': datetime.now() + timedelta(seconds=self.ttl_seconds)
            }

    async def invalidate(self, key: str) -> None:
        """Invalidate specific cache entry"""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]

    async def clear_all(self) -> None:
        """Clear all cache entries"""
        async with self._lock:
            self._cache.clear()

    async def get_stats(self) -> Dict:
        """Get cache statistics"""
        async with self._lock:
            return {
                'entries': len(self._cache),
                'ttl_seconds': self.ttl_seconds,
                'keys': list(self._cache.keys())
            }


# Global cache instance
_cache_instance: Optional[CacheService] = None


def get_cache() -> CacheService:
    """Get global cache instance"""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = CacheService(ttl_seconds=5)
    return _cache_instance
