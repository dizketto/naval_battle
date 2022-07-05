import asyncio

import aioredis


class RedisClient:
    def __init__(self, host, port, password, db):
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.redis = None

    def connect(self):
        self.redis = aioredis.from_url("redis://cache_db", decode_responses=True, db=1)
        return self.redis


redis = RedisClient("localhost", "6379", "vito", 1).connect()
