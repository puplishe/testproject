import pickle

import redis

from ..cache import cache
from ..redis_connection import redis_pool


def invalidate_cache(cache_key_prefix: str, *args, **kwargs):
    serialized_args = pickle.dumps((args, kwargs))
    cache_key = f'{cache_key_prefix}:{serialized_args!r}'
    cache.pop(cache_key, None)
    r = redis.StrictRedis(connection_pool=redis_pool)
    r.delete(cache_key)
