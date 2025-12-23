import functools
import httpx
from fastapi import HTTPException

from app.core.settings import Settings
from app.models.github import GitHubSearchResponse


def handle_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            detail = f"GitHub API error: {e.response.text}"
            raise HTTPException(status_code=status_code, detail=detail)
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"GitHub API unreachable: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    return wrapper


class GitHubClient:
    def __init__(self, settings: Settings) -> None:
        self._base_url = settings.github_base_url

    @handle_errors
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
            
