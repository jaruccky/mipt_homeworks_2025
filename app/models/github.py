from typing import Any
from pydantic import BaseModel


class GitHubRepository(BaseModel):
    name: str
    description: str | None
    html_url: str
    created_at: str
    updated_at: str
    homepage: str | None
    size: int
    stargazers_count: int
    forks_count: int
    open_issues_count: int
    watchers_count: int
    language: str | None
    license: dict[str, Any] | None
    topics: list[str]
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    has_discussions: bool
    fork: bool
    archived: bool
    is_template: bool
    default_branch: str

    @classmethod
    def csv_headers(cls) -> list[str]:
        return list(cls.model_fields.keys())


class GitHubSearchResponse(BaseModel):
    items: list[GitHubRepository]
