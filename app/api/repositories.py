from pathlib import Path

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.settings import Settings
from app.infrastructure.github_client import GitHubClient
from app.services.repositories_service import RepositoriesService
from app.services.csv_writer import CsvWriter

router = APIRouter(tags=["repositories"])


class SearchRepositoriesParams(BaseModel):
    limit: int = Field(gt=0)
    offset: int = Field(0, ge=0)
    lang: str
    stars_min: int = 0
    stars_max: int | None = None
    forks_min: int = 0
    forks_max: int | None = None


def get_settings() -> Settings:
    return Settings()


def get_service(
    settings: Settings = Depends(get_settings),
) -> RepositoriesService:
    github_client = GitHubClient(settings)
    csv_writer = CsvWriter(Path(settings.static_dir))
    return RepositoriesService(github_client, csv_writer)


@router.get("/repositories/search")
async def search_repositories(
    params: SearchRepositoriesParams = Depends(),
    service: RepositoriesService = Depends(get_service),
) -> dict[str, str]:
    filename = await service.search_and_save(**params.model_dump())
    return {
        "status": "ok",
        "file": filename,
    }
