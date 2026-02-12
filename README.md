MatchRight: Resume x Job Matcher
Author: Ali Bidhendi

What this project does
- Takes resume text and job description text
- Uses transformer embeddings to compute a match score (0 to 100)
- Extracts important keywords from the job description
- Shows which keywords are missing from the resume (keyword gap)
- Generates simple, actionable suggestions (only if truthful)

Why this is internship-ready
- Real-world problem (ATS-style matching / candidate-job alignment)
- Uses modern NLP (transformer embeddings)
- Has a clean backend API (FastAPI)
- Has a demo UI recruiters can try (Streamlit)
- Easy to extend: PDF parsing, job database, semantic search, evaluation tests

Tech used
- Python
- sentence-transformers (embeddings)
- scikit-learn (cosine similarity)
- FastAPI (backend API)
- Streamlit (demo UI)

How to run (local)
1) Install dependencies
pip install -r requirements.txt

2) Start the API (from inside matchright/)
uvicorn app.main:app --reload

3) Start the UI (in a second terminal, from inside matchright/)
streamlit run ui/streamlit_app.py

API endpoint
POST /match
Body:
{
  "resume_text": "...",
  "job_text": "..."
}

Returns:
- score: float (0-100)
- missing_keywords: list[str]
- top_resume_keywords: list[str]
- top_job_keywords: list[str]
- suggestions: list[str]
