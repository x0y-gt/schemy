import asyncio
from functools import wraps

def atomic(coro):
    """Decorator to prevent cancellation of the whole web-handler"""

    @wraps(coro)
    async def wrapper(*args, **kwargs):
        try:
            return await asyncio.shield(coro(*args, **kwargs))
        except asyncio.CancelledError:
            # Don't stop inner coroutine on explicit cancel
            raise

    return wrapper
