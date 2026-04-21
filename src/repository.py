from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional

from models import Author, IngestedDocument, Keyword, Paper, Reference


class InMemoryRepository:
    def __init__(self) -> None:
        self._paper_id = 1
        self._author_id = 1
        self._keyword_id = 1
        self._reference_id = 1

        self.papers: Dict[int, Paper] = {}
        self.authors: Dict[str, Author] = {}
        self.keywords: Dict[str, Keyword] = {}
        self.references: Dict[str, Reference] = {}

    def add_document(self, doc: IngestedDocument) -> Paper:
        paper = Paper(
            id=self._paper_id,
            title=doc.title,
            raw_text=doc.raw_text,
            abstract=doc.abstract,
            publication_date=doc.publication_date,
            sentiment=doc.sentiment,
            uploaded_at=datetime.now(timezone.utc),
            authors=list(dict.fromkeys([a.strip() for a in doc.authors if a.strip()])),
            keywords=list(dict.fromkeys([k.strip().lower() for k in doc.keywords if k.strip()])),
            references=list(dict.fromkeys([r.strip() for r in doc.references if r.strip()])),
        )
        self.papers[paper.id] = paper
        self._paper_id += 1

        for author_name in paper.authors:
            key = author_name.lower()
            if key not in self.authors:
                self.authors[key] = Author(id=self._author_id, name=author_name)
                self._author_id += 1

        for kw in paper.keywords:
            if kw not in self.keywords:
                self.keywords[kw] = Keyword(id=self._keyword_id, keyword=kw)
                self._keyword_id += 1

        for ref_title in paper.references:
            key = ref_title.lower()
            if key not in self.references:
                self.references[key] = Reference(id=self._reference_id, referenced_title=ref_title)
                self._reference_id += 1

        return paper

    def all_papers(self) -> List[Paper]:
        return list(self.papers.values())

    def all_authors(self) -> List[Author]:
        return list(self.authors.values())

    def find_papers(
        self,
        author: Optional[str] = None,
        keyword: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
    ) -> List[Paper]:
        records = list(self.papers.values())

        if author:
            needle = author.lower().strip()
            records = [p for p in records if any(a.lower() == needle for a in p.authors)]

        if keyword:
            needle = keyword.lower().strip()
            records = [p for p in records if needle in [k.lower() for k in p.keywords]]

        if year_from is not None:
            records = [p for p in records if p.publication_date is not None and p.publication_date >= year_from]

        if year_to is not None:
            records = [p for p in records if p.publication_date is not None and p.publication_date <= year_to]

        return records

    def reset(self) -> None:
        self.__init__()

    def titles(self) -> Iterable[str]:
        for paper in self.papers.values():
            yield paper.title
