from __future__ import annotations

import re
from collections import defaultdict
from typing import List, Tuple

from gensim.corpora import Dictionary
from gensim.models import LdaModel, TfidfModel
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess

_EXTRA_STOPWORDS = {
    "study",
    "paper",
    "method",
    "results",
    "introduction",
    "conclusion",
    "analysis",
    "research",
}


def _tokenize_documents(text: str) -> List[List[str]]:
    chunks = [c.strip() for c in re.split(r"[\n\.\!\?]+", text) if c.strip()]
    docs: List[List[str]] = []

    for chunk in chunks:
        tokens = [
            t
            for t in simple_preprocess(chunk, deacc=True, min_len=3, max_len=25)
            if t not in STOPWORDS and t not in _EXTRA_STOPWORDS
        ]
        if len(tokens) >= 3:
            docs.append(tokens)

    if docs:
        return docs

    fallback = [
        t
        for t in simple_preprocess(text, deacc=True, min_len=3, max_len=25)
        if t not in STOPWORDS and t not in _EXTRA_STOPWORDS
    ]
    return [fallback] if fallback else []


def extract_topics_and_key_terms(
    text: str,
    num_topics: int = 3,
    words_per_topic: int = 5,
    max_key_terms: int = 12,
) -> Tuple[List[str], List[str]]:
    docs = _tokenize_documents(text)
    if not docs:
        return [], []

    dictionary = Dictionary(docs)
    dictionary.filter_extremes(no_below=1, no_above=0.9, keep_n=5000)
    if len(dictionary) == 0:
        return [], []

    corpus = [dictionary.doc2bow(doc) for doc in docs]
    if not any(corpus):
        return [], []

    tfidf = TfidfModel(corpus, dictionary=dictionary)
    term_scores = defaultdict(float)
    for doc in tfidf[corpus]:
        for token_id, score in doc:
            term_scores[token_id] += float(score)

    key_terms = [
        dictionary[token_id]
        for token_id, _ in sorted(term_scores.items(), key=lambda item: item[1], reverse=True)
    ][:max_key_terms]

    topic_count = min(num_topics, len(dictionary), max(1, len(corpus)))

    topics: List[str] = []
    if topic_count >= 1 and len(corpus) >= 2:
        lda = LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=topic_count,
            random_state=42,
            passes=8,
            iterations=80,
        )
        topic_terms = lda.show_topics(num_topics=topic_count, num_words=words_per_topic, formatted=False)
        topics = [" ".join(word for word, _ in words) for _, words in topic_terms]

    if not topics and key_terms:
        topics = [" ".join(key_terms[:words_per_topic])]

    return topics, key_terms
