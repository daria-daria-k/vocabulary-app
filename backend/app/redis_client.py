import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.environ.get("REDIS_URL")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def get_redis():
    return redis_client

