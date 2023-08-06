import functools
import pickle
import time
from typing import Any

import redis
from cachetools import TTLCache

from .redis_connection import redis_pool

cache: TTLCache[str, Any] = TTLCache(maxsize=100, ttl=600, getsizeof=None,
                                     timer=lambda: int(time.time()))


def cached_with_redis(cache, key_func):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key_prefix = key_func(*args, **kwargs)
            serialized_args = pickle.dumps((args, kwargs))
            cache_key = f'{cache_key_prefix}:{serialized_args}'
            value = cache.get(cache_key)
            if value is None:
                r = redis.StrictRedis(connection_pool=redis_pool)
                serialized_value = r.get(cache_key)
                if serialized_value is not None:
                    value = pickle.loads(serialized_value)
                else:
                    value = func(*args, **kwargs)
                    cache[cache_key] = value
                    r.set(cache_key, pickle.dumps(value))
            return value
        return wrapper
    return decorator
