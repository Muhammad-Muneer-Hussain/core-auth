from redis.asyncio import Redis
from app.core.config import settings

# Global redis client variable to be initialized in lifespan
redis_client: Redis = None

async def init_redis():
    global redis_client
    redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)

async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()

async def add_token_to_blacklist(jti: str, expire_time: int):
    """
    Add token to blacklist with its remaining expiry time.
    jti (JWT ID) or signature can be used. We'll use the token signature as the identifier.
    """
    if redis_client:
        await redis_client.setex(f"bl:{jti}", expire_time, "true")

async def is_token_blacklisted(jti: str) -> bool:
    """
    Check if a token is blacklisted.
    """
    if not redis_client:
        return False
    return await redis_client.exists(f"bl:{jti}") == 1
