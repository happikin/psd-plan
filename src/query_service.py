from __future__ import annotations

from typing import List, Optional

from models import Paper
from repository import InMemoryRepository


def query_papers(
    repository: InMemoryRepository,
    author: Optional[str] = None,
    keyword: Optional[str] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
) -> List[Paper]:
    return repository.find_papers(author=author, keyword=keyword, year_from=year_from, year_to=year_to)

