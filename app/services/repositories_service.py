from app.infrastructure.github_client import GitHubClient
from app.services.csv_writer import CsvWriter
from app.models.github import GitHubRepository


class RepositoriesService:
    def __init__(
        self,
        client: GitHubClient,
        csv_writer: CsvWriter,
    ) -> None:
        self._client = client
        self._csv_writer = csv_writer

    def build_query(
        self,
        lang: str,
        stars_min: int,
        stars_max: int | None,
        forks_min: int,
        forks_max: int | None,
    ) -> str:
        parts = [
            f"language:{lang}",
            f"stars:>={stars_min}",
            f"forks:>={forks_min}",
        ]

        if stars_max is not None:
            parts.append(f"stars:<={stars_max}")
        if forks_max is not None:
            parts.append(f"forks:<={forks_max}")

        return " ".join(parts)

    async def search_and_save(
        self,
        limit: int,
        offset: int,
        lang: str,
        stars_min: int,
        stars_max: int | None,
        forks_min: int,
        forks_max: int | None,
    ) -> str:
        query = self.build_query(
            lang,
            stars_min,
            stars_max,
            forks_min,
            forks_max,
        )

        per_page = 100
        start_page = offset // per_page + 1
        start_index = offset % per_page
        need_total = start_index + limit

        items: list[GitHubRepository] = []
        page = start_page

        while len(items) < need_total:
            response = await self._client.search_repositories(
                query=query,
                per_page=per_page,
                page=page,
            )

            page_items = response.items
            items.extend(page_items)

            if len(page_items) < per_page:
                break

            if page >= 10:
                break

            page += 1

        items = items[start_index : start_index + limit]

        filename = f"repositories_{lang}_{limit}_{offset}.csv"
        await self._csv_writer.write(filename, items)

        return filename
