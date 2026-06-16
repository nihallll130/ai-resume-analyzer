# Project: AI Resume Analyzer & ATS Optimizer
# Author: Your Full Name
# GitHub: github.com/your-username

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

REQUIRED_SECTIONS = ["experience", "education", "skills", "summary", "projects"]

def calculate_ats_score(resume_text: str, jd_text: str) -> dict:
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    keyword_score = round(similarity * 100, 2)

    found = sum(1 for s in REQUIRED_SECTIONS if s in resume_text.lower())
    section_score = (found / len(REQUIRED_SECTIONS)) * 100

    has_email = bool(re.search(r"[\w.]+@[\w.]+", resume_text))
    has_phone = bool(re.search(r"\d{10}|\d{3}[-.\s]\d{3}[-.\s]\d{4}", resume_text))
    format_score = ((has_email + has_phone) / 2) * 100

    final = (keyword_score * 0.6) + (section_score * 0.25) + (format_score * 0.15)
    return {
        "ats_score": round(final, 1),
        "keyword_score": keyword_score,
        "section_score": section_score,
        "sections_found": found
    }
