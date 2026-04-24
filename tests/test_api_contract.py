from __future__ import annotations

import asyncio

import pytest
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError

import app as backend_app
from models import IngestedDocument


def _seed_documents() -> list[int]:
    ids: list[int] = []

    doc_a = backend_app.repo.add_document(
        IngestedDocument(
            title="Graph Mining 101",
            raw_text="raw-a",
            abstract="abstract-a",
            publication_date=2020,
            sentiment="neutral",
            authors=["Alice", "Bob"],
            keywords=["ai", "graphs"],
            topics=["topic a"],
            key_terms=["graph"],
            references=[],
        )
    )
    ids.append(doc_a.id)

    doc_b = backend_app.repo.add_document(
        IngestedDocument(
            title="Applied NLP",
            raw_text="raw-b",
            abstract="abstract-b",
            publication_date=2022,
            sentiment="positive",
            authors=["Alice"],
            keywords=["ai", "nlp"],
            topics=["topic b"],
            key_terms=["nlp"],
            references=[],
        )
    )
    ids.append(doc_b.id)

    doc_c = backend_app.repo.add_document(
        IngestedDocument(
            title="Systems Paper",
            raw_text="raw-c",
            abstract="abstract-c",
            publication_date=None,
            sentiment="neutral",
            authors=["Cara"],
            keywords=["systems"],
            topics=["topic c"],
            key_terms=["systems"],
            references=[],
        )
    )
    ids.append(doc_c.id)

    return ids


def test_documents_list_contract_includes_pagination_and_summary_only() -> None:
    backend_app.repo.reset()
    _seed_documents()

    payload = backend_app.list_documents(
        author=None,
        keyword=None,
        year_from=None,
        year_to=None,
        sort_by="title",
        sort_order="asc",
        page=1,
        page_size=2,
    )
    assert payload.total == 3
    assert payload.page == 1
    assert payload.page_size == 2
    assert payload.total_pages == 2
    assert payload.has_next is True
    assert payload.has_prev is False
    assert len(payload.items) == 2
    assert [item.title for item in payload.items] == ["Applied NLP", "Graph Mining 101"]
    assert all("raw_text" not in item.model_dump() for item in payload.items)


def test_documents_list_contract_page_out_of_range_is_empty() -> None:
    backend_app.repo.reset()
    _seed_documents()

    payload = backend_app.list_documents(
        author=None,
        keyword=None,
        year_from=None,
        year_to=None,
        sort_by="uploaded_at",
        sort_order="desc",
        page=10,
        page_size=2,
    )
    assert payload.total == 3
    assert payload.total_pages == 2
    assert payload.items == []
    assert payload.has_next is False
    assert payload.has_prev is True


def test_document_detail_contract_returns_full_payload() -> None:
    backend_app.repo.reset()
    paper_ids = _seed_documents()

    payload = backend_app.document_detail(paper_ids[0])
    assert payload.id == paper_ids[0]
    assert payload.raw_text == "raw-a"

    with pytest.raises(HTTPException) as error:
        backend_app.document_detail(99999)
    assert error.value.status_code == 404
    assert error.value.detail == "Paper not found"


def test_graph_contract_uses_stable_types_and_relationships() -> None:
    backend_app.repo.reset()
    _seed_documents()

    payload = backend_app.graph().model_dump()

    node_types = {node["type"] for node in payload["nodes"]}
    edge_types = {edge["relationship"] for edge in payload["edges"]}

    assert node_types.issubset({"paper", "author", "keyword"})
    assert edge_types.issubset({"written_by", "tagged_with", "coauthor"})


def test_timeline_contract_is_sparse_by_year() -> None:
    backend_app.repo.reset()
    _seed_documents()

    payload = backend_app.timeline(keyword="ai")
    assert [p.model_dump() for p in payload] == [{"year": 2020, "count": 1}, {"year": 2022, "count": 1}]


def test_standard_error_schema_for_http_and_validation_errors() -> None:
    scope = {"type": "http", "method": "GET", "path": "/", "headers": []}
    request = Request(scope)
    request.state.request_id = "req-test-1"

    http_response = asyncio.run(
        backend_app.http_exception_handler(
            request,
            HTTPException(status_code=404, detail="Paper not found"),
        )
    )
    assert http_response.status_code == 404
    assert http_response.body is not None
    assert b'"code":"HTTP_404"' in http_response.body
    assert b'"request_id":"req-test-1"' in http_response.body

    validation_error = RequestValidationError([{"loc": ("query", "keyword"), "msg": "bad", "type": "value_error"}])
    validation_response = asyncio.run(
        backend_app.request_validation_exception_handler(request, validation_error)
    )
    assert validation_response.status_code == 422
    assert b'"code":"REQUEST_VALIDATION_ERROR"' in validation_response.body


def test_openapi_contract_exposes_typed_models() -> None:
    schema = backend_app.app.openapi()
    paths = schema["paths"]
    components = schema["components"]["schemas"]

    assert "/documents" in paths
    assert "/documents/{paper_id}" in paths
    assert "DocumentListResponse" in components
    assert "APIErrorResponse" in components
