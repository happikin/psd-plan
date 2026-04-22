from __future__ import annotations

from collections import Counter
from typing import List

from models import TimelinePoint
from repository import InMemoryRepository


def keyword_timeline(repository: InMemoryRepository, keyword: str) -> List[TimelinePoint]:
    needle = keyword.lower().strip()
    yearly = Counter()

    for paper in repository.all_papers():
        if paper.publication_date is None:
            continue
        if needle in [k.lower() for k in paper.keywords]:
            yearly[paper.publication_date] += 1

    return [TimelinePoint(year=year, count=count) for year, count in sorted(yearly.items())]

