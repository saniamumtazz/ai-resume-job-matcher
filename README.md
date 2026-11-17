<div align="center">

# 🎯 AI Resume & Job Matcher

### Smart Career Assistant

Upload a resume, paste a job description, and get an **explainable match score**, honest improvement suggestions, interview preparation and a downloadable PDF report.

![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-TF--IDF-F7931E?logo=scikitlearn&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-NLP-09A3D5)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?logo=openai&logoColor=white)
![Tests](https://img.shields.io/badge/tests-36%20passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

[🎬 Demo video](docs/demo/live_demo.mp4) · [🚀 Live app](#) · [⚙️ Setup guide](docs/SETUP_GUIDE.md)

![Dashboard](docs/screenshots/dashboard.png)

</div>

---

## 📌 Overview

Job seekers often send the same resume to every job without knowing how well it fits. I built **AI Resume & Job Matcher** to answer three questions:

1. **How well does my resume match this job?** - with a score I can actually explain.
2. **What am I missing?** - required and preferred skills, resume quality gaps.
3. **How do I prepare?** - honest resume suggestions and job-specific interview questions.

I designed the app to be **transparent and honest**: the score comes from a visible formula (not a black box), the AI is told never to invent skills or experience, and the app clearly states that the score is **not an official ATS score**.

> 💡 The app works **without an API key** too (offline mode), so anyone can try it instantly with the built-in demo data.

---

## ✨ Features

| | Feature | Details |
|---|---|---|
| 📄 | **Resume upload** | PDF & DOCX, validation by type / size / file signature, clear errors for empty, corrupted, password-protected or unsupported files |
| 📋 | **Job description analyzer** | Separates required vs preferred skills; extracts experience, qualifications, responsibilities and keywords |
| 🎯 | **Matching engine** | Explainable score, matched / missing / additional skills, per-component breakdown |
| 💡 | **AI resume improvement** | Summary rewrite, suggestions and ATS-friendly bullets; strict "never invent experience" prompts; editable output with review confirmation |
| 🎤 | **Interview preparation** | Technical, skill-gap and HR questions with sample answers |
| 📊 | **Dashboard** | Score gauge, breakdown chart, skills donut, resume quality indicators, suggestions and interview preview |
| ⬇️ | **Export** | PDF analysis report, suggestions (TXT), interview questions (TXT) |
| 🔒 | **Privacy-first** | Files processed in memory only, API key in `.env`, per-session AI call limit |

---

## 📸 Screenshots

### Resume Analyzer
Extracts text, detects skills by category and runs 11 resume quality checks.

![Resume Analyzer](docs/screenshots/resume_analyzer.png)

### Job Matcher
Required vs preferred skills, experience and qualifications from the job description, plus the explainable match score.

![Job Matcher](docs/screenshots/job_matcher.png)

### Resume Improvement
Suggestions and rewrites based only on facts already in the resume. Everything is editable and must be reviewed before download.

![Resume Improvement](docs/screenshots/improvement.png)

### Interview Preparation
Job-specific technical, gap and HR questions with sample answers.

![Interview Preparation](docs/screenshots/interview.png)

### Demo video
A full walkthrough (upload → match → improve → interview → dashboard): [`docs/demo/live_demo.mp4`](docs/demo/live_demo.mp4)

---

## 🧮 How the match score works

The score is the sum of four weighted components. Weights are defined in [`config.py`](config.py).

| Component | Weight | What it measures |
|---|:---:|---|
| Required skills coverage | 50% | Share of the job's required skills found in the resume |
| Preferred skills coverage | 20% | Share of the nice-to-have skills found |
| Keyword similarity | 20% | TF-IDF cosine similarity between resume and job text (0.5+ counts as 100%) |
| Experience fit | 10% | Years detected in the resume vs years requested |

If a job description does not mention a component (for example, no preferred skills), its weight is shared proportionally among the remaining components. The dashboard shows every component's score, weight and points.

> ⚠️ This is an **estimated score from this app's own formula**. It is not an official ATS score and no real ATS is used.

---

## 🏗️ Architecture

```
Resume (PDF/DOCX) -> resume_parser ----\
                                        +--> matching_engine --> Streamlit dashboard
Job description  -> job_analyzer ------/             |
                                                     +--> ai_service (OpenAI + offline fallback)
                                                     +--> interview_generator
                                                     +--> report_generator (PDF / TXT)
```

**Design decisions**

- **Skill detection is rule-based** (curated skills database + spaCy `PhraseMatcher`), not AI. It is fast, free, reproducible and cannot hallucinate skills. AI is used only for writing suggestions and questions.
- **AI is optional.** If there is no key, the key is invalid, or the API fails, the app falls back to rule-based output instead of crashing.
- **Prompt safety.** Prompts forbid inventing employers, degrees, tools or metrics, and treat resume/job text as data, not instructions.
- **UI has no business logic.** Pages only call functions from `src/`, which keeps the logic testable.

---

## 🛠️ Tech stack

| Area | Tools |
|---|---|
| Language & UI | Python, Streamlit |
| NLP & ML | spaCy (tokenizer + PhraseMatcher), scikit-learn (TF-IDF, cosine similarity) |
| Data | Pandas |
| File parsing | PyMuPDF (PDF), python-docx (DOCX) |
| AI | OpenAI API |
| Visualisation | Plotly |
| Reports | ReportLab |
| Config & security | python-dotenv, `.env`, Streamlit secrets |
| Testing | pytest |

---

## 📁 Project structure

```
ai-resume-job-matcher/
├── app.py                      # Dashboard + navigation
├── config.py                   # weights, limits, model, API key loading
├── requirements.txt
├── .env.example                # copy to .env and add your key (optional)
├── src/
│   ├── skills_db.py            # skills + aliases, PhraseMatcher extraction
│   ├── resume_parser.py        # validation, PDF/DOCX extraction, quality checks
│   ├── job_analyzer.py         # required/preferred skills, experience, keywords
│   ├── matching_engine.py      # explainable scoring
│   ├── ai_service.py           # OpenAI integration + rule-based fallback
│   ├── interview_generator.py  # technical / gap / HR questions
│   ├── report_generator.py     # PDF and TXT exports
│   └── ui_helpers.py           # charts, chips, session state
├── pages/                      # Resume Analyzer, Job Matcher, Improvement, Interview, About
├── tests/                      # pytest suite (36 tests)
├── sample_data/                # fictional sample resume + sample job description
└── docs/                       # screenshots, demo video, setup & deployment guides
```

---

## 🚀 Getting started

### Prerequisites
- Python 3.11 or 3.12
- (Optional) an OpenAI API key for AI-written suggestions

### Installation

```bash
git clone https://github.com/saniamumtazz/ai-resume-job-matcher.git
cd ai-resume-job-matcher

python -m venv .venv
# Windows:    .venv\Scripts\activate
# Mac/Linux:  source .venv/bin/activate

pip install -r requirements.txt
```

### Configure (optional)

```bash
# Windows: copy .env.example .env      Mac/Linux: cp .env.example .env
```

Open `.env` and set `OPENAI_API_KEY=your_key`. Skip this step to use offline mode.

### Run

```bash
streamlit run app.py
```

Open <http://localhost:8501> and click **Load demo data** on the dashboard to see everything in one click.

Beginner-friendly guide with common errors: [`docs/SETUP_GUIDE.md`](docs/SETUP_GUIDE.md)

---

## 🧭 Usage

1. **Resume Analyzer** - upload a PDF/DOCX resume and review extracted text, skills and quality checks.
2. **Job Matcher** - paste a job description and click *Analyze & Match*.
3. **Resume Improvement** - generate suggestions, edit them, tick the review box and download.
4. **Interview Preparation** - choose how many questions you want and generate them.
5. **Dashboard** - see the full picture and export the PDF report.

---

## ✅ Testing

```bash
python -m pytest -q
```

36 tests cover file validation (empty, oversized, fake and corrupted PDF/DOCX), text extraction, skill aliases, job-description parsing, score calculation and weight redistribution, AI failure fallback (mocked), and PDF export with special characters.

---

## 🔐 Security & privacy

- API keys are loaded from `.env` or Streamlit secrets and are never hard-coded; `.env` is git-ignored.
- Uploaded files are validated and processed **in memory**; nothing is written to disk.
- Resume text is sent to OpenAI **only** when an AI feature is used and a key is configured.
- AI usage is capped per session (`MAX_AI_CALLS_PER_SESSION`, default 10).

**API cost:** OpenAI's API is pay-as-you-go and separate from a ChatGPT subscription. The default model is `gpt-4o-mini` (change with `OPENAI_MODEL`). One request uses a few thousand tokens. Check OpenAI's pricing page for current rates.

---

## ☁️ Deployment

The app can be deployed free on **Streamlit Community Cloud** (main file: `app.py`, Python 3.12). Put `OPENAI_API_KEY` in the app's *Secrets*, never in the repository. Full steps: [`docs/GITHUB_AND_DEPLOYMENT.md`](docs/GITHUB_AND_DEPLOYMENT.md).

---

## 🧠 What I learned

- Building an **explainable scoring system** instead of a black box, and handling edge cases like missing components.
- Parsing messy real-world input (PDF layouts, DOCX tables, scanned files) and failing gracefully.
- Designing **safe AI prompts** and graceful fallbacks so the app never depends on a single API.
- Structuring a Streamlit project into testable modules and writing tests for parsing, scoring and failure paths.

---

## ⚠️ Limitations

- Skills are detected from a curated list in `src/skills_db.py`; skills outside the list are not detected (the list is easy to extend).
- No OCR, so scanned image-only PDFs are not supported.
- Experience years are estimated from dates in the Experience section.
- The score is an estimate for self-improvement, not an official ATS score.
- AI-generated content must always be reviewed by the user.

## 🛣️ Roadmap

- [ ] OCR support for scanned resumes
- [ ] Semantic similarity with embeddings
- [ ] Compare one resume against multiple jobs
- [ ] Export the improved resume as DOCX
- [ ] Larger skills ontology and more languages

---

## 👩‍💻 Author

**Sania Mumtaz** - BCA graduate, aspiring Data Analyst / Data Scientist

[![GitHub](https://img.shields.io/badge/GitHub-saniamumtazz-181717?logo=github)](https://github.com/saniamumtazz)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-sania--mumtaz-0A66C2?logo=linkedin)](https://linkedin.com/in/sania-mumtaz)

## 📄 License

Released under the [MIT License](LICENSE).

---

<div align="center">⭐ If you find this project useful, please give it a star!</div>
