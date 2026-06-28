# MatchRight Resume Job Matcher

MatchRight is a FastAPI and Streamlit app that compares resume text against a job description, calculates a semantic match score, identifies keyword gaps, and returns practical suggestions.

It is built as a portfolio-ready NLP project for candidate-job alignment. The backend exposes a clean API, while the Streamlit UI gives recruiters, students, or job seekers a simple way to test resume/job fit locally.

## What it does

MatchRight takes two inputs:

- resume text
- job description text

Then it returns:

- semantic match score from 0 to 100
- missing job-description keywords
- top resume keywords
- top job-description keywords
- simple suggestions based on the detected keyword gap

## Why this project exists

Many resume tools only count exact keyword matches. MatchRight adds semantic comparison with transformer embeddings so the score can reflect meaning, not just repeated words.

The current version is intentionally focused and readable. It shows a complete NLP workflow with an API layer, schema validation, embedding-based similarity, keyword extraction, and a lightweight browser UI.

## Features

- FastAPI backend with `/match` endpoint
- Streamlit demo UI
- Sentence-transformer embeddings
- Cosine similarity scoring
- Resume/job keyword extraction
- Missing keyword detection
- Practical suggestion generation
- Pydantic request and response models
- Local-first workflow for testing and demos

## Tech stack

- Python
- FastAPI
- Streamlit
- sentence-transformers
- scikit-learn
- NumPy
- Pydantic
- Uvicorn
- Requests

## Project structure

```text
README.md
requirements.txt
app/
  init.py
  main.py
  nlp.py
  schemas.py
ui/
  streamlit_app.py
```

## Install

Clone the repository:

```bash
git clone https://github.com/LazyPanda902/matchright-resume-job-matcher.git
cd matchright-resume-job-matcher
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the API

Start the FastAPI backend:

```bash
uvicorn app.main:app --reload
```

The API will run locally, usually at:

```text
http://localhost:8000
```

FastAPI interactive docs are available at:

```text
http://localhost:8000/docs
```

## Run the UI

Open a second terminal and start the Streamlit app:

```bash
streamlit run ui/streamlit_app.py
```

Paste resume text, paste job-description text, confirm the API URL, and run the match.

## API usage

Endpoint:

```text
POST /match
```

Request body:

```json
{
  "resume_text": "Python developer with FastAPI, Docker, and SQL experience...",
  "job_text": "We need a backend engineer with Python, FastAPI, REST APIs, Docker, and PostgreSQL..."
}
```

Example response:

```json
{
  "score": 82.41,
  "missing_keywords": ["postgresql", "rest", "backend"],
  "top_resume_keywords": ["python", "fastapi", "docker"],
  "top_job_keywords": ["python", "fastapi", "postgresql"],
  "suggestions": [
    "If truthful, add experience or examples related to: postgresql.",
    "If truthful, add experience or examples related to: rest."
  ]
}
```

## How scoring works

The NLP engine in `app/nlp.py` uses `SentenceTransformer` to convert resume and job text into embedding vectors.

The app then calculates cosine similarity between those vectors:

```python
sim = float(cosine_similarity([r_vec], [j_vec])[0][0])
return round(sim * 100.0, 2)
```

This gives a semantic match score from 0 to 100.

## Keyword gap analysis

The keyword engine extracts common tokens from the job description and resume text, removes simple stopwords, ranks tokens by frequency, and compares the two sets.

This produces a practical gap list that helps identify missing terms or concepts from the resume.

## Current limitations

- The keyword extractor is intentionally lightweight.
- It does not parse PDF or DOCX resumes yet.
- It does not verify whether a suggestion is true for the candidate.
- It should not be used as an automated hiring decision system.
- Scores should be treated as guidance, not proof of fit.

## Planned improvements

- Add PDF and DOCX resume parsing.
- Add tests for scoring and keyword gap behavior.
- Add example fixtures for resume/job pairs.
- Add CI checks.
- Add a screenshot or GIF demo.
- Add exportable match reports.
- Add optional weighting for required vs preferred job skills.

## Privacy and security

MatchRight is designed to run locally. Resume text and job descriptions entered into the local Streamlit UI are sent to the local FastAPI backend URL configured in the UI.

Do not paste sensitive personal information into any deployed or public instance unless you control the server and understand how logs, browser history, and network traffic are handled.

## License

Add a license before using this project outside personal portfolio/demo work.
