import os

from redis.asyncio import Redis
from redis.exceptions import RedisError
from dotenv import load_dotenv
load_dotenv()

redis_client = Redis.from_url(
    os.getenv("REDIS_URL","redis://localhost:6379/0"),
    decode_responses=True,
)

CACHE_TTL_SECONDS = 3600

def cache_key(short_code:str)->str:
    return f"short-url:{short_code}"

async def check_redis_connection():
    try:
        await redis_client.ping()
        return True
    except RedisError:
        return False

async def get_cached_url(short_code:str)->str|None:
    try:
        return await redis_client.get(cache_key(short_code))
    except RedisError:
        return None


async def cache_url(short_code:str,original_url:str) -> None:
    try:
        await redis_client.set(
            cache_key(short_code),
            original_url,
            ex=CACHE_TTL_SECONDS
        )
    except RedisError:
        pass