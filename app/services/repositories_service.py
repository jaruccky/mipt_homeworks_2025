from pathlib import Path
from typing import Any
from aiofile import async_open

from app.infrastructure.github_client import GitHubClient


STATIC_DIR = Path("app/static")
STATIC_DIR.mkdir(parents=True, exist_ok=True)

CSV_HEADER: list[str] = [
    "Name",
    "Description",
    "URL",
    "Created At",
    "Updated At",
    "Homepage",
    "Size",
    "Stars",
    "Forks",
    "Issues",
    "Watchers",
    "Language",
    "License",
    "Topics",
    "Has Issues",
    "Has Projects",
    "Has Downloads",
    "Has Wiki",
    "Has Pages",
    "Has Discussions",
    "Is Fork",
    "Is Archived",
    "Is Template",
    "Default Branch",
]


def build_query(
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


def _csv_escape(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    if "," in text or '"' in text or "\n" in text:
        text = text.replace('"', '""')
        return f'"{text}"'
    return text


async def search_and_save_repositories(
    limit: int,
    offset: int,
    lang: str,
    stars_min: int,
    stars_max: int | None,
    forks_min: int,
    forks_max: int | None,
) -> str:
    client = GitHubClient()

    query = build_query(
        lang=lang,
        stars_min=stars_min,
        stars_max=stars_max,
        forks_min=forks_min,
        forks_max=forks_max,
    )

    per_page = min(100, limit)
    page = offset // per_page + 1

    response = await client.search_repositories(
        query=query,
        per_page=per_page,
        page=page,
    )

    items: list[dict[str, Any]] = response.get("items", [])
    items = items[offset % per_page : offset % per_page + limit]

    filename = f"repositories_{lang}_{limit}_{offset}.csv"
    filepath = STATIC_DIR / filename

    async with async_open(filepath, "w", encoding="utf-8") as file:
        # header
        await file.write(",".join(CSV_HEADER) + "\n")

        for repo in items:
            license_name = repo["license"]["name"] if repo.get("license") else ""
            topics = ";".join(repo.get("topics", []))

            row = [
                repo.get("name"),
                repo.get("description"),
                repo.get("html_url"),
                repo.get("created_at"),
                repo.get("updated_at"),
                repo.get("homepage"),
                repo.get("size"),
                repo.get("stargazers_count"),
                repo.get("forks_count"),
                repo.get("open_issues_count"),
                repo.get("watchers_count"),
                repo.get("language"),
                license_name,
                topics,
                repo.get("has_issues"),
                repo.get("has_projects"),
                repo.get("has_downloads"),
                repo.get("has_wiki"),
                repo.get("has_pages"),
                repo.get("has_discussions"),
                repo.get("fork"),
                repo.get("archived"),
                repo.get("is_template"),
                repo.get("default_branch"),
            ]

            escaped_row = [_csv_escape(v) for v in row]
            await file.write(",".join(escaped_row) + "\n")

    return filename
