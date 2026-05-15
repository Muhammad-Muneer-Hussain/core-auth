from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import auth, users
from app.redis.client import init_redis, close_redis
from app.db.session import engine
from app.models.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_redis()
    # Create DB tables for local SQLite testing
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await close_redis()
    await engine.dispose()

app = FastAPI(title="CORE-AUTH API", lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
