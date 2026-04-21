from __future__ import annotations

import re
from typing import List


def extract_references(text: str) -> List[str]:
    marker = re.search(r"\breferences\b", text, flags=re.IGNORECASE)
    if not marker:
        return []

    tail = text[marker.end():]
    lines = [line.strip(" -\t") for line in tail.splitlines()]
    refs = []
    for line in lines:
        if not line:
            continue
        if len(line) < 8:
            continue
        refs.append(line)
        if len(refs) >= 30:
            break
    return refs

