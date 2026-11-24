from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.db.base import Base
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем таблицы при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Shop API",
    description="Интернет-магазин: управление товарами",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(api_router)

@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "service": "Shop API"}