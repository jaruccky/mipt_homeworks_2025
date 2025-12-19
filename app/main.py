from fastapi import FastAPI

from app.api.repositories import router as repositories_router

app = FastAPI(title="GitHub Repositories Search")

app.include_router(repositories_router, prefix="/api")
