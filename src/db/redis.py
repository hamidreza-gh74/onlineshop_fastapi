import redis.asyncio as redis
from src.config import config


token_blocklist = redis.from_url(config.REDIS_URL)

JTI_EXPIRY = 3600  #1 HOUR




async def add_jti_to_blocklist(jti:str) -> None:
    await token_blocklist.set(
        name=jti,
        value= "",
        ex= JTI_EXPIRY
    )

async def token_in_blocklist(jti:str)-> bool:
    jti = await token_blocklist.get(jti)

    return jti is not None