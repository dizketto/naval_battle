import asyncio
from contextlib import asynccontextmanager

contextual_locks = {}

# aioredis locking didn't seem to work well so decided for asyncio locking instead.
# a single task queue (concurrency = 1) would have been handy for this instead of locking.
# nevertheless it would introduce other kind of topics to be handled,
# like result backends, result polling or pub/sub messaging for the client
# to be aware of the success/failure of the operation


@asynccontextmanager
async def get_lock(named_resource):
    if not contextual_locks.get(named_resource):
        contextual_locks[named_resource] = asyncio.Lock()

    async with contextual_locks[named_resource]:
        yield

    if not contextual_locks[named_resource]._waiters:
        del contextual_locks[named_resource]
