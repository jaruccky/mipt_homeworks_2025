from pathlib import Path
from typing import Iterable, Any

from aiofile import async_open

from app.models.github import GitHubRepository


class CsvWriter:
    def __init__(self, static_dir: Path) -> None:
        self.static_dir = static_dir

    def _escape(self, value: Any) -> str:
        if value is None:
            return ""
        text = str(value)
        if any(ch in text for ch in [",", '"', "\n"]):
            text = text.replace('"', '""')
            return f'"{text}"'
        return text

    async def write(
        self,
        filename: str,
        items: Iterable[GitHubRepository],
    ) -> None:
        filepath = self.static_dir / filename

        async with async_open(filepath, "w", encoding="utf-8") as file:
            await file.write(",".join(GitHubRepository.csv_headers()) + "\n")

            for repo in items:
                values = repo.model_dump().values()
                escaped = [self._escape(v) for v in values]
                await file.write(",".join(escaped) + "\n")
