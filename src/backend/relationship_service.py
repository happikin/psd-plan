from __future__ import annotations

from typing import Dict, List, Set, Tuple

from repository import Repository


def coauthor_edges(repository: Repository) -> List[Tuple[str, str]]:
    edges: Set[Tuple[str, str]] = set()
    for paper in repository.all_papers():
        authors = sorted(set(paper.authors))
        for i, left in enumerate(authors):
            for right in authors[i + 1:]:
                edges.add((left, right))
    return sorted(edges)


def author_topic_links(repository: Repository) -> Dict[str, List[str]]:
    mapping: Dict[str, Set[str]] = {}
    for paper in repository.all_papers():
        for author in paper.authors:
            mapping.setdefault(author, set()).update(paper.keywords)
    return {author: sorted(topics) for author, topics in mapping.items()}
