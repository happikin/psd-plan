from __future__ import annotations

import re
from collections import Counter
from typing import List

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "in", "is", "it", "of",
    "on", "or", "that", "the", "to", "was", "were", "with", "we", "this", "these", "those", "our", "their",
    "into", "about", "using", "used", "than", "also", "can", "may", "not", "which", "will", "within", "across",
}


def extract_keywords(text: str, top_n: int = 8) -> List[str]:
    tokens = re.findall(r"[a-zA-Z][a-zA-Z\-]{2,}", text.lower())
    filtered = [t for t in tokens if t not in STOPWORDS]
    counts = Counter(filtered)
    return [word for word, _ in counts.most_common(top_n)]

