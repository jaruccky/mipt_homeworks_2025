from typing import Any

import httpx


class GitHubClient:
    BASE_URL = "https://api.github.com"

    async def search_repositories(
        self,
        query: str,
        per_page: int,
        page: int,
    ) -> Any:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/search/repositories",
                params={
                    "q": query,
                    "per_page": per_page,
                    "page": page,
                },
                headers={
                    "Accept": "application/vnd.github+json",
                },
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
