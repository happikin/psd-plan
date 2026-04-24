from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AuthConfig:
    enabled: bool = False
    provider: str = "none"
    audience: str = ""
    issuer: str = ""


@dataclass(frozen=True)
class AuthContext:
    subject: str
    role: str


class AuthScaffold:
    """
    Internal-only scaffold for future auth integration.
    Not wired into API routes or middleware.
    """

    def __init__(self, config: AuthConfig | None = None) -> None:
        self.config = config or AuthConfig()

    def parse_bearer_token(self, authorization_header: Optional[str]) -> Optional[str]:
        if not authorization_header or not authorization_header.startswith("Bearer "):
            return None
        token = authorization_header.removeprefix("Bearer ").strip()
        return token or None

    def validate_token(self, token: str) -> Optional[AuthContext]:
        # Placeholder: real token verification is intentionally not active yet.
        if not self.config.enabled or not token:
            return None
        return None
