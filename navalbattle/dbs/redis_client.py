import asyncio

import aioredis


class RedisClient:
    @staticmethod
    def connect():
        redis = aioredis.from_url("redis://cache_db", decode_responses=True, db=1)
        return redis


redis = RedisClient.connect()
