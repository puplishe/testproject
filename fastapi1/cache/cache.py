import json

import aioredis

from .redis_connection import redis_pool


class RedisCache:
    def __init__(self, ttl=600) -> None:

        self.ttl = ttl
        self.redis = None

    async def connect(self) -> aioredis.Redis:
        """"Connection to redis"""
        self.redis = await redis_pool

    async def setcache(self, key, value: bytes):
        """"Creates cache for given data and key"""
        if self.redis is None:
            await self.connect()
        else:
            await self.redis.setex(name=key, value=json.dumps(value), time=self.ttl)

    async def get_cache(self, key):
        """"Returns cached data or None"""
        if self.redis is None:
            await self.connect()
        cache = await self.redis.get(key)
        if cache:
            return json.loads(cache)
        return None

    async def flush_cache(self):
        """"Flushes all stored cache"""
        if self.redis is None:
            await self.connect()
        await self.redis.flushdb()

    async def delete_cache(self, key):
        if self.redis is None:
            await self.connect()
        await self.redis.delete(key)

    async def invalidate_cache(self, key):
        """"Deletes cache for given key"""
        if self.redis is None:
            await self.connect()
        keys = await self.redis.keys(f'{key}*')
        if keys:
            await self.redis.delete(*keys)
