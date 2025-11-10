from dataclasses import dataclass, field
from typing import Protocol, TypeVar

from homework_oop.src.dto import BaseDTO, GithubRepoDTO
from homework_oop.src.repositories import BaseRepository

T = TypeVar("T")


@dataclass(kw_only=True)
class DataFrame(Protocol[T]):
    repository: BaseRepository
    _data: BaseDTO = field(init=False)

    def __post_init__(self): ...

    def select(self): ...

    def sort(self): ...

    def groub_by(self):
        pass


class GitHubDataFrame(DataFrame[GithubRepoDTO]):
    def __post_init__(self):
        self._data = self.repository.read(GitHubDataFrame)

    # def select(self, fields: list[str]): ...
