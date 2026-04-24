from __future__ import annotations

from datetime import datetime
from typing import Any, List, Literal, Optional

from pydantic import BaseModel, Field


class Reference(BaseModel):
    id: int
    referenced_title: str


class Author(BaseModel):
    id: int
    name: str
    credibility_score: int = 0


class Keyword(BaseModel):
    id: int
    keyword: str


class Paper(BaseModel):
    id: int
    title: str
    raw_text: str
    abstract: str
    publication_date: Optional[int] = None
    sentiment: str = "neutral"
    uploaded_at: datetime
    authors: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    topics: List[str] = Field(default_factory=list)
    key_terms: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)


class IngestedDocument(BaseModel):
    title: str
    raw_text: str
    abstract: str
    publication_date: Optional[int] = None
    sentiment: str = "neutral"
    authors: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    topics: List[str] = Field(default_factory=list)
    key_terms: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)


class TimelinePoint(BaseModel):
    year: int
    count: int


class GraphNode(BaseModel):
    id: str
    label: str
    type: Literal["paper", "author", "keyword"]
    score: Optional[int] = None


class GraphEdge(BaseModel):
    source: str
    target: str
    relationship: Literal["written_by", "tagged_with", "coauthor"]


class GraphPayload(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]


class HealthResponse(BaseModel):
    status: str


class DocumentUploadResponse(BaseModel):
    paper_id: int
    title: str
    authors: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    topics: List[str] = Field(default_factory=list)
    key_terms: List[str] = Field(default_factory=list)
    publication_date: Optional[int] = None


class PaperSummary(BaseModel):
    id: int
    title: str
    abstract: str
    publication_date: Optional[int] = None
    sentiment: str = "neutral"
    uploaded_at: datetime
    authors: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    topics: List[str] = Field(default_factory=list)
    key_terms: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)


class DocumentListResponse(BaseModel):
    items: List[PaperSummary] = Field(default_factory=list)
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class ResetResponse(BaseModel):
    status: str


class BootstrapResponse(BaseModel):
    loaded: int
    parsed: int
    failed: int
    skipped: int
    used_cache: bool


class APIErrorResponse(BaseModel):
    code: str
    message: str
    details: Any = None
    request_id: str
