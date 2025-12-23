import httpx
from fastapi import HTTPException

from app.core.settings import Settings
from app.models.github import GitHubSearchResponse


class GitHubClient:
    def __init__(self, settings: Settings) -> None:
        self._base_url = settings.github_base_url

    async def search_repositories(
        self,
        query: str,
        per_page: int,
        page: int,
    ) -> GitHubSearchResponse:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._base_url}/search/repositories",
                params={
                    "q": query,
                    "per_page": per_page,
                    "page": page,
                },
                headers={
                    "Accept": "application/vnd.github+json",
                },
            )
            response.raise_for_status()
            return GitHubSearchResponse.model_validate(response.json())
