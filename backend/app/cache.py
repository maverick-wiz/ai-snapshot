"""
In-memory TTL cache for news (5-min) and stocks (10-sec).
AISNP-17 · Owner: OMEGA
"""
import time
import asyncio
from typing import Any, Optional


class TTLCache:
    def __init__(self):
        self._store: dict[str, tuple[Any, float]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            if key in self._store:
                value, expires_at = self._store[key]
                if time.time() < expires_at:
                    return value
                del self._store[key]
        return None

    async def set(self, key: str, value: Any, ttl: int) -> None:
        async with self._lock:
            self._store[key] = (value, time.time() + ttl)

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._store.pop(key, None)


# Global cache instance
cache = TTLCache()

NEWS_TTL = 300   # 5 minutes
STOCKS_TTL = 10  # 10 seconds
