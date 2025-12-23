from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.api.repositories import router
from app.core.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()

    static_dir = Path(settings.static_dir)
    static_dir.mkdir(parents=True, exist_ok=True)

    yield


app = FastAPI(
    title="GitHub Repositories Search",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api")
