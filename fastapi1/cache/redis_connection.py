import os

import aioredis as redis
from dotenv import load_dotenv

load_dotenv()
redis_pool = redis.Redis(
    host=os.getenv('REDIS_HOST'), port=6379, db=0, decode_responses=True)
