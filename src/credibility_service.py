from __future__ import annotations

import re
from typing import Dict

from repository import InMemoryRepository


def _normalize(text: str) -> str:
    return re.sub(r"\W+", "", text.lower())


def recompute_credibility(repository: InMemoryRepository) -> Dict[str, int]:
    title_to_authors = {_normalize(p.title): p.authors for p in repository.all_papers()}
    scores: Dict[str, int] = {author.name.lower(): 0 for author in repository.all_authors()}

    for paper in repository.all_papers():
        for ref in paper.references:
            normalized_ref = _normalize(ref)
            for normalized_title, authors in title_to_authors.items():
                if not normalized_ref:
                    continue
                if normalized_title in normalized_ref or normalized_ref in normalized_title:
                    for author in authors:
                        scores[author.lower()] = scores.get(author.lower(), 0) + 1

    for key, author in repository.authors.items():
        author.credibility_score = scores.get(key, 0)

    return scores

