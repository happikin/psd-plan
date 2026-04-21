from __future__ import annotations

from datetime import datetime
from typing import List, Optional

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
    references: List[str] = Field(default_factory=list)


class IngestedDocument(BaseModel):
    title: str
    raw_text: str
    abstract: str
    publication_date: Optional[int] = None
    sentiment: str = "neutral"
    authors: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)


class TimelinePoint(BaseModel):
    year: int
    count: int


class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    score: Optional[int] = None


class GraphEdge(BaseModel):
    source: str
    target: str
    relationship: str


class GraphPayload(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]

