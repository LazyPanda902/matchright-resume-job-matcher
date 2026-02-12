"""
MatchRight NLP Engine
Author: Ali Bidhendi

Main tasks:
1) Compute semantic similarity between resume and job description
2) Extract job keywords and find what is missing from the resume
3) Return suggestions based on the gap

Why embeddings:
- Keyword matching alone misses meaning.
- Embeddings capture semantic similarity better.

How scoring works:
- Embed resume and job text into vectors (SentenceTransformer)
- Compute cosine similarity
- Convert to percentage (0 to 100)
"""

import re
from typing import List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


_MODEL = None


def get_model() -> SentenceTransformer:
    """
    Load the model once (lazy-load).
    Keeps API fast after the first request.
    """
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _MODEL


def clean_text(text: str) -> str:
    """
    Basic cleaning to reduce noise.
    """
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def embed(text: str) -> np.ndarray:
    """
    Convert text to an embedding vector.
    normalize_embeddings=True helps cosine similarity.
    """
    model = get_model()
    return model.encode([text], normalize_embeddings=True)[0]


def similarity_score(resume_text: str, job_text: str) -> float:
    """
    Returns similarity from 0 to 100.
    """
    r_vec = embed(clean_text(resume_text))
    j_vec = embed(clean_text(job_text))

    sim = float(cosine_similarity([r_vec], [j_vec])[0][0])
    return round(sim * 100.0, 2)


def simple_keywords(text: str, top_k: int = 20) -> List[str]:
    """
    Lightweight keyword extraction for MVP.
    - Pull tokens
    - Remove common stopwords
    - Rank by frequency
    """
    text = clean_text(text)
    tokens = re.findall(r"[a-zA-Z\+\#\.]{2,}", text)

    stop = {
        "and", "or", "the", "a", "an", "to", "of", "in", "for", "with", "on", "at",
        "is", "are", "this", "that", "as", "by", "be", "from", "you", "we", "our",
        "their", "your", "will", "can", "may", "have", "has", "had", "using"
    }

    tokens = [t for t in tokens if t not in stop]

    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1

    ranked = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return [w for w, _ in ranked[:top_k]]


def keyword_gap_analysis(
    resume_text: str,
    job_text: str,
    job_top_k: int = 20
) -> Tuple[List[str], List[str], List[str]]:
    """
    Compare top keywords from job description against resume keywords.

    Returns:
    - missing keywords from the resume
    - top resume keywords (for display)
    - top job keywords (for display)
    """
    resume_kw_set = set(simple_keywords(resume_text, top_k=60))
    job_top = simple_keywords(job_text, top_k=job_top_k)

    missing = [w for w in job_top if w not in resume_kw_set]
    resume_top = list(resume_kw_set)[:job_top_k]

    return missing, resume_top, job_top


def suggestions_from_missing(missing: List[str]) -> List[str]:
    """
    Turn missing keywords into resume improvement suggestions.
    """
    if not missing:
        return [
            "Your resume already matches most key terms. Improve clarity and add measurable impact.",
            "Add 2–3 quantified bullets (performance, accuracy, cost, time).",
            "Mirror job wording in your bullets only if it is truthful."
        ]

    return [
        f"Add these keywords if they are truly part of your experience: {', '.join(missing[:10])}",
        "Rewrite 2–3 bullets to match the job wording (tools, frameworks, role keywords).",
        "Add measurable results (time saved, accuracy improved, performance increased)."
    ]
