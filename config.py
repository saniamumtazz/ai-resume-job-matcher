"""Central configuration. Nothing secret is hardcoded here."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

APP_NAME = "AI Resume & Job Matcher"
APP_TAGLINE = "Smart Career Assistant"
APP_VERSION = "1.0.0"

# ---------- OpenAI ----------
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TIMEOUT_SECONDS = 60
AI_MAX_OUTPUT_TOKENS = 1800
MAX_AI_INPUT_CHARS = 6000          # resume/JD text is truncated before sending
MAX_AI_CALLS_PER_SESSION = int(os.getenv("MAX_AI_CALLS_PER_SESSION", "10"))

# ---------- File validation ----------
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "5"))
ALLOWED_EXTENSIONS = (".pdf", ".docx")
MAX_PDF_PAGES = 15
MIN_RESUME_CHARS = 100
MAX_JD_CHARS = 15000
MIN_JD_CHARS = 50

# ---------- Scoring (transparent, shown in the About page) ----------
WEIGHTS = {
    "required_skills": 50,
    "preferred_skills": 20,
    "keyword_similarity": 20,
    "experience": 10,
}
# A TF-IDF cosine similarity of this value (or higher) counts as 100%.
SIMILARITY_FULL_SCORE_AT = 0.5

SCORE_LABELS = [  # (minimum score, label)
    (80, "Excellent match"),
    (65, "Good match"),
    (45, "Moderate match"),
    (0, "Low match"),
]

DISCLAIMER = (
    "This is an estimated match score calculated by this app's own transparent "
    "formula. It is NOT an official ATS score and no real ATS is used."
)

SAMPLE_DIR = BASE_DIR / "sample_data"


def get_openai_api_key() -> str:
    """Return the API key from .env / environment / Streamlit secrets, or ''."""
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        try:
            import streamlit as st

            key = str(st.secrets.get("OPENAI_API_KEY", "")).strip()
        except Exception:  # no secrets file configured
            key = ""
    if key in {"your_openai_api_key_here", "sk-your-key-here"}:
        return ""
    return key
