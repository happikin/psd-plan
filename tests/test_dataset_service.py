from pathlib import Path

from dataset_service import bootstrap_repository, load_parsed_jsonl, parse_papers_to_jsonl
from repository import InMemoryRepository


def test_parse_papers_to_jsonl_and_load(monkeypatch, tmp_path: Path) -> None:
    papers_dir = tmp_path / "Papers"
    papers_dir.mkdir()
    (papers_dir / "a.pdf").write_bytes(b"pdf-a")
    (papers_dir / "b.pdf").write_bytes(b"pdf-b")

    parsed_path = tmp_path / "data" / "parsed" / "papers.jsonl"

    def fake_parse_pdf_text(data: bytes) -> str:
        if data == b"pdf-a":
            return "Paper A\nAlice\nAbstract: A reliable model\nPublished 2020\nKeywords: ai, graph"
        if data == b"pdf-b":
            return "Paper B\nBob\nAbstract: A robust model\nPublished 2021\nKeywords: ai, timeline\nReferences\nPaper A"
        raise ValueError("bad data")

    monkeypatch.setattr("dataset_service.parse_pdf_text", fake_parse_pdf_text)

    parsed, failed = parse_papers_to_jsonl(papers_dir, parsed_path)
    assert parsed == 2
    assert failed == 0
    assert parsed_path.exists()

    repo = InMemoryRepository()
    loaded = load_parsed_jsonl(repo, parsed_path)
    assert loaded == 2
    assert len(repo.all_papers()) == 2


def test_bootstrap_uses_cache_when_available(monkeypatch, tmp_path: Path) -> None:
    parsed_path = tmp_path / "data" / "parsed" / "papers.jsonl"
    parsed_path.parent.mkdir(parents=True, exist_ok=True)
    parsed_path.write_text(
        '{"title":"Cached Paper","raw_text":"t","abstract":"a","publication_date":2024,"sentiment":"neutral","authors":["Alice"],"keywords":["ai"],"references":[],"source_file":"x.pdf"}\n',
        encoding="utf-8",
    )

    repo = InMemoryRepository()

    def should_not_be_called(*args, **kwargs):
        raise AssertionError("parse path should not run when cache exists")

    monkeypatch.setattr("dataset_service.parse_papers_to_jsonl", should_not_be_called)

    result = bootstrap_repository(
        repo,
        papers_dir=tmp_path / "Papers",
        parsed_output_path=parsed_path,
        force_reparse=False,
    )

    assert result["used_cache"] is True
    assert result["loaded"] == 1
    assert len(repo.all_papers()) == 1

