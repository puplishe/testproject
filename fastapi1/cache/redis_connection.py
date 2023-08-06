import os

import redis
from dotenv import load_dotenv

load_dotenv()
redis_pool = redis.ConnectionPool(
    host=os.getenv('REDIS_HOST'), port=6379, db=0)
