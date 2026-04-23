from metadata_extractor import extract_metadata
from models import IngestedDocument
from repository import InMemoryRepository
from timeline_service import keyword_timeline
from credibility_service import recompute_credibility


def test_extract_metadata_keywords_and_references() -> None:
    text = """
    Efficient Graph Mining for Literature Analysis
    Alice Smith, Bob Jones
    Abstract: We present a robust and reliable method for analysis.
    Keywords: graph mining, literature, citation analysis
    Published 2022

    References
    Efficient Graph Mining for Literature Analysis
    Another Relevant Study
    """

    metadata = extract_metadata(text)

    assert metadata["title"] == "Efficient Graph Mining for Literature Analysis"
    assert metadata["authors"] == ["Alice Smith", "Bob Jones"]
    assert "graph mining" in metadata["keywords"]
    assert len(metadata["topics"]) >= 1
    assert len(metadata["key_terms"]) >= 1
    assert metadata["publication_date"] == 2022
    assert len(metadata["references"]) >= 2


def test_extract_metadata_prefers_pdf_and_layout_signals() -> None:
    text = """
    This Should Not Be Chosen As Title
    Wrong Line For Authors
    Abstract: short text for checks.
    Published 2024
    """

    metadata = extract_metadata(
        text,
        pdf_title="Reliable PDF Title",
        pdf_author="Alice Smith, Bob Jones",
        layout_title="Layout Title",
        layout_authors=["Layout Person"],
    )

    assert metadata["title"] == "Reliable PDF Title"
    assert metadata["authors"] == ["Alice Smith", "Bob Jones"]


def test_credibility_score_and_timeline() -> None:
    repo = InMemoryRepository()

    repo.add_document(
        IngestedDocument(
            title="Paper A",
            raw_text="text",
            abstract="abstract",
            publication_date=2021,
            sentiment="neutral",
            authors=["Alice"],
            keywords=["nlp", "graphs"],
            references=[],
        )
    )

    repo.add_document(
        IngestedDocument(
            title="Paper B",
            raw_text="text",
            abstract="abstract",
            publication_date=2022,
            sentiment="neutral",
            authors=["Bob"],
            keywords=["nlp"],
            references=["Paper A"],
        )
    )

    scores = recompute_credibility(repo)

    assert scores["alice"] == 1
    assert scores["bob"] == 0

    points = keyword_timeline(repo, "nlp")
    assert [p.year for p in points] == [2021, 2022]
    assert [p.count for p in points] == [1, 1]
