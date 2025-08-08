from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import redis.asyncio as aioredis
import os

router = APIRouter()
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

@router.websocket("/ws/prices/{symbol}")
async def ws_prices(websocket: WebSocket, symbol: str):
    await websocket.accept()
    r = aioredis.from_url(REDIS_URL, decode_responses=True)
    pubsub = r.pubsub()
    channel = f"prices.{symbol}"
    await pubsub.subscribe(channel)
    try:
        async for msg in pubsub.listen():
            if msg["type"] == "message":
                await websocket.send_text(msg["data"])
    except WebSocketDisconnect:
        pass
    finally:
        await pubsub.unsubscribe(channel)
        await r.close()
