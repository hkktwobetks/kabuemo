from fastapi import FastAPI
from app.api.routers import health
from app.api import ws as ws_router

app = FastAPI()
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(ws_router.router) 

@app.get("/healthz")
def healthz():
    return {"ok": True}
