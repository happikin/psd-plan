from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional, Protocol

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

from models import Author, IngestedDocument, Keyword, Paper, Reference


def _dedupe_by_key(values: List[str], key_fn) -> List[str]:
    seen: set[str] = set()
    ordered: List[str] = []
    for value in values:
        key = key_fn(value)
        if key in seen:
            continue
        seen.add(key)
        ordered.append(value)
    return ordered


class Repository(Protocol):
    def add_document(self, doc: IngestedDocument) -> Paper: ...
    def all_papers(self) -> List[Paper]: ...
    def all_authors(self) -> List[Author]: ...
    def find_papers(
        self,
        author: Optional[str] = None,
        keyword: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
    ) -> List[Paper]: ...
    def get_paper(self, paper_id: int) -> Optional[Paper]: ...
    def reset(self) -> None: ...
    def titles(self) -> Iterable[str]: ...
    def set_author_credibility(self, scores: Dict[str, int]) -> None: ...


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
        authors = _dedupe_by_key([a.strip() for a in doc.authors if a.strip()], lambda x: x.lower())
        references = _dedupe_by_key([r.strip() for r in doc.references if r.strip()], lambda x: x.lower())
        paper = Paper(
            id=self._paper_id,
            title=doc.title,
            raw_text=doc.raw_text,
            abstract=doc.abstract,
            publication_date=doc.publication_date,
            sentiment=doc.sentiment,
            uploaded_at=datetime.now(timezone.utc),
            authors=authors,
            keywords=list(dict.fromkeys([k.strip().lower() for k in doc.keywords if k.strip()])),
            topics=list(dict.fromkeys([t.strip().lower() for t in doc.topics if t.strip()])),
            key_terms=list(dict.fromkeys([k.strip().lower() for k in doc.key_terms if k.strip()])),
            references=references,
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

    def get_paper(self, paper_id: int) -> Optional[Paper]:
        return self.papers.get(paper_id)

    def set_author_credibility(self, scores: Dict[str, int]) -> None:
        for key, author in self.authors.items():
            author.credibility_score = scores.get(key, 0)

    def reset(self) -> None:
        self.__init__()

    def titles(self) -> Iterable[str]:
        for paper in self.papers.values():
            yield paper.title


class Base(DeclarativeBase):
    pass


class PaperRecord(Base):
    __tablename__ = "papers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    abstract: Mapped[str] = mapped_column(Text, nullable=False)
    publication_date: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sentiment: Mapped[str] = mapped_column(String(32), nullable=False, default="neutral")
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    authors: Mapped[List[PaperAuthorRecord]] = relationship(back_populates="paper", cascade="all, delete-orphan")
    keywords: Mapped[List[PaperKeywordRecord]] = relationship(back_populates="paper", cascade="all, delete-orphan")
    topics: Mapped[List[PaperTopicRecord]] = relationship(back_populates="paper", cascade="all, delete-orphan")
    key_terms: Mapped[List[PaperKeyTermRecord]] = relationship(back_populates="paper", cascade="all, delete-orphan")
    references: Mapped[List[PaperReferenceRecord]] = relationship(back_populates="paper", cascade="all, delete-orphan")


class AuthorRecord(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    name_key: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    credibility_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class KeywordRecord(Base):
    __tablename__ = "keywords"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    keyword: Mapped[str] = mapped_column(String(255), nullable=False)
    keyword_key: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)


class ReferenceRecord(Base):
    __tablename__ = "references"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    referenced_title: Mapped[str] = mapped_column(String(1024), nullable=False)
    title_key: Mapped[str] = mapped_column(String(1024), unique=True, index=True, nullable=False)


class PaperAuthorRecord(Base):
    __tablename__ = "paper_authors"

    paper_id: Mapped[int] = mapped_column(ForeignKey("papers.id", ondelete="CASCADE"), primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), primary_key=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    paper: Mapped[PaperRecord] = relationship(back_populates="authors")
    author: Mapped[AuthorRecord] = relationship()


class PaperKeywordRecord(Base):
    __tablename__ = "paper_keywords"

    paper_id: Mapped[int] = mapped_column(ForeignKey("papers.id", ondelete="CASCADE"), primary_key=True)
    keyword_id: Mapped[int] = mapped_column(ForeignKey("keywords.id"), primary_key=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    paper: Mapped[PaperRecord] = relationship(back_populates="keywords")
    keyword: Mapped[KeywordRecord] = relationship()


class PaperTopicRecord(Base):
    __tablename__ = "paper_topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    paper_id: Mapped[int] = mapped_column(ForeignKey("papers.id", ondelete="CASCADE"), index=True)
    topic: Mapped[str] = mapped_column(String(512), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    paper: Mapped[PaperRecord] = relationship(back_populates="topics")


class PaperKeyTermRecord(Base):
    __tablename__ = "paper_key_terms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    paper_id: Mapped[int] = mapped_column(ForeignKey("papers.id", ondelete="CASCADE"), index=True)
    key_term: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    paper: Mapped[PaperRecord] = relationship(back_populates="key_terms")


class PaperReferenceRecord(Base):
    __tablename__ = "paper_references"

    paper_id: Mapped[int] = mapped_column(ForeignKey("papers.id", ondelete="CASCADE"), primary_key=True)
    reference_id: Mapped[int] = mapped_column(ForeignKey("references.id"), primary_key=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    paper: Mapped[PaperRecord] = relationship(back_populates="references")
    reference: Mapped[ReferenceRecord] = relationship()


class SQLRepository:
    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        Base.metadata.create_all(self.engine)

    def _paper_to_model(self, record: PaperRecord) -> Paper:
        return Paper(
            id=record.id,
            title=record.title,
            raw_text=record.raw_text,
            abstract=record.abstract,
            publication_date=record.publication_date,
            sentiment=record.sentiment,
            uploaded_at=record.uploaded_at,
            authors=[x.author.name for x in sorted(record.authors, key=lambda a: a.position)],
            keywords=[x.keyword.keyword for x in sorted(record.keywords, key=lambda k: k.position)],
            topics=[x.topic for x in sorted(record.topics, key=lambda t: t.position)],
            key_terms=[x.key_term for x in sorted(record.key_terms, key=lambda t: t.position)],
            references=[x.reference.referenced_title for x in sorted(record.references, key=lambda r: r.position)],
        )

    def add_document(self, doc: IngestedDocument) -> Paper:
        authors = _dedupe_by_key([a.strip() for a in doc.authors if a.strip()], lambda x: x.lower())
        keywords = list(dict.fromkeys([k.strip().lower() for k in doc.keywords if k.strip()]))
        topics = list(dict.fromkeys([t.strip().lower() for t in doc.topics if t.strip()]))
        key_terms = list(dict.fromkeys([k.strip().lower() for k in doc.key_terms if k.strip()]))
        references = _dedupe_by_key([r.strip() for r in doc.references if r.strip()], lambda x: x.lower())

        with self.SessionLocal() as session:
            paper = PaperRecord(
                title=doc.title,
                raw_text=doc.raw_text,
                abstract=doc.abstract,
                publication_date=doc.publication_date,
                sentiment=doc.sentiment,
                uploaded_at=datetime.now(timezone.utc),
            )
            session.add(paper)
            session.flush()

            for idx, name in enumerate(authors):
                key = name.lower()
                author = session.scalar(select(AuthorRecord).where(AuthorRecord.name_key == key))
                if author is None:
                    author = AuthorRecord(name=name, name_key=key)
                    session.add(author)
                    session.flush()
                session.add(PaperAuthorRecord(paper_id=paper.id, author_id=author.id, position=idx))

            for idx, kw in enumerate(keywords):
                keyword = session.scalar(select(KeywordRecord).where(KeywordRecord.keyword_key == kw))
                if keyword is None:
                    keyword = KeywordRecord(keyword=kw, keyword_key=kw)
                    session.add(keyword)
                    session.flush()
                session.add(PaperKeywordRecord(paper_id=paper.id, keyword_id=keyword.id, position=idx))

            for idx, topic in enumerate(topics):
                session.add(PaperTopicRecord(paper_id=paper.id, topic=topic, position=idx))

            for idx, key_term in enumerate(key_terms):
                session.add(PaperKeyTermRecord(paper_id=paper.id, key_term=key_term, position=idx))

            for idx, ref_title in enumerate(references):
                key = ref_title.lower()
                ref = session.scalar(select(ReferenceRecord).where(ReferenceRecord.title_key == key))
                if ref is None:
                    ref = ReferenceRecord(referenced_title=ref_title, title_key=key)
                    session.add(ref)
                    session.flush()
                session.add(PaperReferenceRecord(paper_id=paper.id, reference_id=ref.id, position=idx))

            session.commit()
            session.refresh(paper)
            return self._paper_to_model(paper)

    def all_papers(self) -> List[Paper]:
        with self.SessionLocal() as session:
            papers = session.scalars(select(PaperRecord)).all()
            return [self._paper_to_model(p) for p in papers]

    def all_authors(self) -> List[Author]:
        with self.SessionLocal() as session:
            rows = session.scalars(select(AuthorRecord)).all()
            return [Author(id=r.id, name=r.name, credibility_score=r.credibility_score) for r in rows]

    def find_papers(
        self,
        author: Optional[str] = None,
        keyword: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
    ) -> List[Paper]:
        with self.SessionLocal() as session:
            stmt = select(PaperRecord).distinct()
            if author:
                stmt = stmt.join(PaperAuthorRecord).join(AuthorRecord).where(AuthorRecord.name_key == author.lower().strip())
            if keyword:
                stmt = stmt.join(PaperKeywordRecord).join(KeywordRecord).where(
                    KeywordRecord.keyword_key == keyword.lower().strip()
                )
            if year_from is not None:
                stmt = stmt.where(PaperRecord.publication_date.is_not(None), PaperRecord.publication_date >= year_from)
            if year_to is not None:
                stmt = stmt.where(PaperRecord.publication_date.is_not(None), PaperRecord.publication_date <= year_to)

            rows = session.scalars(stmt).all()
            return [self._paper_to_model(r) for r in rows]

    def get_paper(self, paper_id: int) -> Optional[Paper]:
        with self.SessionLocal() as session:
            record = session.get(PaperRecord, paper_id)
            if record is None:
                return None
            return self._paper_to_model(record)

    def set_author_credibility(self, scores: Dict[str, int]) -> None:
        with self.SessionLocal() as session:
            for row in session.scalars(select(AuthorRecord)).all():
                row.credibility_score = scores.get(row.name_key, 0)
            session.commit()

    def reset(self) -> None:
        with self.SessionLocal() as session:
            session.query(PaperReferenceRecord).delete()
            session.query(PaperKeyTermRecord).delete()
            session.query(PaperTopicRecord).delete()
            session.query(PaperKeywordRecord).delete()
            session.query(PaperAuthorRecord).delete()
            session.query(PaperRecord).delete()
            session.query(ReferenceRecord).delete()
            session.query(KeywordRecord).delete()
            session.query(AuthorRecord).delete()
            session.commit()

    def titles(self) -> Iterable[str]:
        with self.SessionLocal() as session:
            for title in session.scalars(select(PaperRecord.title)).all():
                yield title


def create_repository() -> Repository:
    database_url = os.getenv("DATABASE_URL", "sqlite:///./data/corehub.db")
    return SQLRepository(database_url)
