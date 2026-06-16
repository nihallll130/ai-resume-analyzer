# Project: AI Resume Analyzer & ATS Optimizer
# Author: Your Full Name
# GitHub: github.com/nihallll130

import streamlit as st
import tempfile
import os

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("AI Resume Analyzer & ATS Optimizer")

# Lazy imports — load only when needed
@st.cache_resource
def load_modules():
    from parser import extract_text
    from ats_scorer import calculate_ats_score
    from keyword_matcher import get_missing_keywords
    from bullet_improver import improve_bullets
    return extract_text, calculate_ats_score, get_missing_keywords, improve_bullets

col1, col2 = st.columns(2)
with col1:
    uploaded = st.file_uploader("Upload your resume", type=["pdf","docx","txt"])
with col2:
    jd_text = st.text_area("Paste the job description", height=200)

if uploaded and jd_text:
    extract_text, calculate_ats_score, get_missing_keywords, improve_bullets = load_modules()

    with tempfile.NamedTemporaryFile(delete=False,
         suffix=os.path.splitext(uploaded.name)[1]) as f:
        f.write(uploaded.read())
        temp_path = f.name

    resume_text = extract_text(temp_path)
    tab1, tab2, tab3 = st.tabs(["ATS Score", "Keywords", "Improve Bullets"])

    with tab1:
        result = calculate_ats_score(resume_text, jd_text)
        st.metric("Overall ATS Score", f"{result['ats_score']} / 100")
        st.progress(result['ats_score'] / 100)
        st.write(f"Keyword match: {result['keyword_score']}%")
        st.write(f"Sections found: {result['sections_found']} / 5")

    with tab2:
        kw = get_missing_keywords(resume_text, jd_text)
        st.success(f"Matched: {', '.join(kw['matched'])}")
        st.error(f"Missing: {', '.join(kw['missing'])}")
        st.metric("Keyword Match Rate", f"{kw['match_rate']}%")

    with tab3:
        bullets_input = st.text_area("Paste bullet points (one per line)")
        if st.button("Improve with AI") and bullets_input:
            bullets = [b.strip() for b in bullets_input.split("\n") if b.strip()]
            with st.spinner("Rewriting with AI..."):
                improved = improve_bullets(bullets, jd_text)
            for orig, new in zip(bullets, improved):
                st.markdown(f"**Before:** {orig}")
                st.markdown(f"**After:** {new}")
                st.divider()
else:
    st.info("👆 Upload your resume and paste a job description to get started!")
