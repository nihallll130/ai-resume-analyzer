from collections import Counter

def extract_keywords(text: str, top_n: int = 30) -> list:
    import re
    # Simple keyword extraction without spaCy
    # Remove special characters and split into words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Common stop words to remove
    stop_words = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all',
        'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day',
        'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new',
        'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'she',
        'use', 'way', 'will', 'with', 'have', 'this', 'that',
        'from', 'they', 'been', 'more', 'when', 'your', 'said',
        'each', 'which', 'their', 'time', 'about', 'would',
        'there', 'could', 'other', 'into', 'than', 'then',
        'some', 'these', 'also', 'what', 'were', 'must', 'just'
    }
    
    keywords = [w for w in words if w not in stop_words]
    return [kw for kw, _ in Counter(keywords).most_common(top_n)]

def get_missing_keywords(resume_text: str, jd_text: str) -> dict:
    jd_keywords = set(extract_keywords(jd_text))
    resume_keywords = set(extract_keywords(resume_text))
    
    if not jd_keywords:
        return {"matched": [], "missing": [], "match_rate": 0.0}
    
    missing = jd_keywords - resume_keywords
    matched = jd_keywords & resume_keywords
    return {
        "matched": sorted(matched),
        "missing": sorted(missing),
        "match_rate": round(len(matched) / len(jd_keywords) * 100, 1)
    }
