"""
MatchRight UI (Streamlit)
Author: Ali Bidhendi

This is the demo interface.
It calls the FastAPI backend.

Run:
streamlit run ui/streamlit_app.py
"""

import streamlit as st
import requests


st.title("MatchRight: Resume x Job Matcher")
st.caption("By Ali Bidhendi")

resume = st.text_area(
    "Paste Resume Text",
    height=220,
    placeholder="Paste your resume text here..."
)

job = st.text_area(
    "Paste Job Description Text",
    height=220,
    placeholder="Paste the job description here..."
)

api_url = st.text_input("API URL", value="http://localhost:8000/match")

if st.button("Run Match"):
    if not resume.strip() or not job.strip():
        st.warning("Please paste BOTH resume text and job description text.")
    else:
        try:
            resp = requests.post(
                api_url,
                json={"resume_text": resume, "job_text": job},
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()

            st.metric("Match Score", f"{data['score']} / 100")

            st.subheader("Missing Keywords (from JD)")
            st.write(data["missing_keywords"])

            st.subheader("Suggestions")
            for s in data["suggestions"]:
                st.write("- " + s)

            st.subheader("Top Keywords (JD)")
            st.write(data["top_job_keywords"])

        except Exception as e:
            st.error(f"Error calling API: {e}")
