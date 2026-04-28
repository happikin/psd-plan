import pytest

import repository


def test_create_repository_defaults_to_sqlite(monkeypatch):
    monkeypatch.delenv("DB_MODE", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    repo = repository.create_repository()
    assert isinstance(repo, repository.SQLRepository)
    assert repo.database_url == "sqlite:///./data/corehub.db"


def test_create_repository_postgres_requires_database_url(monkeypatch):
    monkeypatch.setenv("DB_MODE", "postgres")
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(ValueError, match="requires DATABASE_URL"):
        repository.create_repository()


def test_create_repository_postgres_requires_psycopg_url(monkeypatch):
    monkeypatch.setenv("DB_MODE", "postgres")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/corehub")

    with pytest.raises(ValueError, match=r"postgresql\+psycopg"):
        repository.create_repository()


def test_create_repository_accepts_postgres_psycopg_url(monkeypatch):
    monkeypatch.setenv("DB_MODE", "postgres")
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://user:pass@localhost:5432/corehub")

    # Avoid real connection/schema work in this config-only test.
    called = {}

    def fake_init(self, database_url: str) -> None:
        called["database_url"] = database_url
        self.database_url = database_url

    monkeypatch.setattr(repository.SQLRepository, "__init__", fake_init)

    repo = repository.create_repository()
    assert isinstance(repo, repository.SQLRepository)
    assert called["database_url"] == "postgresql+psycopg://user:pass@localhost:5432/corehub"


def test_unsupported_db_mode_raises(monkeypatch):
    monkeypatch.setenv("DB_MODE", "mysql")
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(ValueError, match="Unsupported DB_MODE"):
        repository.create_repository()
