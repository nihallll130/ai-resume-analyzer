# Project: AI Resume Analyzer & ATS Optimizer
# Author: Your Full Name
# GitHub: github.com/your-username

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a professional resume writer.
Rewrite resume bullet points to be more impactful using strong
action verbs, quantify results where possible, and align with
the job description."""

def improve_bullets(bullets: list, jd_text: str) -> list:
    improved = []
    for bullet in bullets:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Job Description:\n{jd_text[:500]}\n\nBullet:\n{bullet}"}
            ],
            max_tokens=150
        )
        improved.append(response.choices[0].message.content.strip())
    return improved
