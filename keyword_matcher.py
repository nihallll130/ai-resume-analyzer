# Project: AI Resume Analyzer & ATS Optimizer
# Author: Your Full Name
# GitHub: github.com/your-username

import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text: str, top_n: int = 30) -> list:
    doc = nlp(text.lower())
    keywords = [
        token.lemma_ for token in doc
        if token.pos_ in ("NOUN", "PROPN", "ADJ")
        and not token.is_stop
        and len(token.text) > 2
    ]
    return [kw for kw, _ in Counter(keywords).most_common(top_n)]

def get_missing_keywords(resume_text: str, jd_text: str) -> dict:
    jd_keywords = set(extract_keywords(jd_text))
    resume_keywords = set(extract_keywords(resume_text))
    missing = jd_keywords - resume_keywords
    matched = jd_keywords & resume_keywords
    return {
        "matched": sorted(matched),
        "missing": sorted(missing),
        "match_rate": round(len(matched) / len(jd_keywords) * 100, 1)
    }
