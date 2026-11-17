"""AI Resume & Job Matcher - main entry point (Dashboard + navigation).

Run with:  streamlit run app.py
"""
import streamlit as st

import config
from src import ui_helpers as ui
from src.report_generator import build_pdf_report, improvements_to_text, interview_to_text

st.set_page_config(page_title=f"{config.APP_NAME}", page_icon="🎯", layout="wide")
ui.setup_app()


def dashboard() -> None:
    ui.page_header(f"🎯 {config.APP_NAME}", f"{config.APP_TAGLINE} - upload a resume, paste a job, get an explainable match.")
    resume, job, match = (st.session_state.get(k) for k in ("resume", "job", "match"))

    if match is None:
        st.markdown("### Get started in 3 steps")
        c1, c2, c3 = st.columns(3)
        for col, icon, head, text in [
            (c1, "📄", "1. Upload resume", "Open **Resume Analyzer** and upload a PDF or DOCX."),
            (c2, "📋", "2. Paste job", "Open **Job Matcher** and paste a job description."),
            (c3, "🚀", "3. Improve & prepare", "See your score, improve your resume and practise interview questions."),
        ]:
            with col, st.container(border=True):
                st.markdown(f"### {icon}")
                st.markdown(f"**{head}**")
                st.write(text)
        st.markdown("#### Just want to see it work?")
        if st.button("▶️ Load demo data (fictional resume + sample job)", type="primary"):
            ui.load_demo()
            st.rerun()
        ui.privacy_note()
        return

    st.markdown(f"#### Target role: {job.title or 'Pasted job description'}  \n"
                f"<span class='small-note'>Resume: {resume.filename}</span>", unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns(5)
    req_total = len(job.required_skills)
    metrics = [
        (m1, "Match score", f"{match.score:.0f}%", match.label),
        (m2, "Required skills", f"{len(match.matched_required)}/{req_total}" if req_total else "n/a", "matched"),
        (m3, "Matched skills", str(len(match.matched_skills)), None),
        (m4, "Missing skills", str(len(match.missing_skills)), None),
        (m5, "Resume quality", f"{resume.quality_score}/100", None),
    ]
    for col, label, value, delta in metrics:
        with col, st.container(border=True):
            st.metric(label, value, delta, delta_color="off" if delta else "normal")

    g1, g2, g3 = st.columns([1, 1.3, 1])
    g1.plotly_chart(ui.gauge(match.score), width="stretch")
    g2.plotly_chart(ui.breakdown_chart(match), width="stretch")
    g3.plotly_chart(ui.skills_donut(match), width="stretch")
    st.caption("⚠️ " + config.DISCLAIMER)

    left, right = st.columns(2)
    with left, st.container(border=True):
        st.markdown("#### ✅ Matched skills")
        ui.chips(match.matched_skills, "green", "None yet")
    with right, st.container(border=True):
        st.markdown("#### ❌ Missing skills")
        ui.chips(match.missing_required, "red", "No required skills missing 🎉")
        ui.chips(match.missing_preferred, "gray")

    with st.container(border=True):
        st.markdown("#### 📊 Resume quality indicators")
        cols = st.columns(2)
        for i, q in enumerate(resume.quality):
            cols[i % 2].markdown(f"{'✅' if q.passed else '⚠️'} {q.label}")

    imp, iv = st.session_state.get("improvements"), st.session_state.get("interview")
    with st.container(border=True):
        st.markdown("#### 💡 Improvement suggestions")
        if imp:
            for s in imp.suggestions[:5]:
                st.markdown(f"- {s}")
            st.caption("See the Resume Improvement page for the full list and editable summary.")
        else:
            st.caption("Not generated yet. Open **Resume Improvement** and click Generate.")
    with st.container(border=True):
        st.markdown("#### 🎤 Interview preparation")
        if iv:
            for q in iv.questions[:4]:
                st.markdown(f"- **{q['type']}**: {q['question']}")
            st.caption(f"{len(iv.questions)} questions ready on the Interview Preparation page.")
        else:
            st.caption("Not generated yet. Open **Interview Preparation** and click Generate.")

    st.markdown("#### ⬇️ Export")
    d1, d2, d3 = st.columns(3)
    d1.download_button("📑 Analysis report (PDF)", build_pdf_report(resume, job, match, imp, iv),
                       "resume_analysis_report.pdf", "application/pdf", width="stretch")
    if imp:
        d2.download_button("📝 Improvement suggestions (TXT)",
                           improvements_to_text(imp.summary, imp.suggestions, imp.bullets, imp.source),
                           "resume_improvements.txt", width="stretch")
    else:
        d2.button("📝 Improvement suggestions (generate first)", disabled=True, width="stretch")
    if iv:
        d3.download_button("🎤 Interview questions (TXT)", interview_to_text(iv),
                           "interview_questions.txt", width="stretch")
    else:
        d3.button("🎤 Interview questions (generate first)", disabled=True, width="stretch")


with st.sidebar:
    st.markdown(f"### 🎯 {config.APP_NAME}")
    st.caption(config.APP_TAGLINE)

pages = [
    st.Page(dashboard, title="Dashboard", icon="🏠", default=True),
    st.Page("pages/1_Resume_Analyzer.py", title="Resume Analyzer", icon="📄"),
    st.Page("pages/2_Job_Matcher.py", title="Job Matcher", icon="📋"),
    st.Page("pages/3_Resume_Improvement.py", title="Resume Improvement", icon="💡"),
    st.Page("pages/4_Interview_Preparation.py", title="Interview Preparation", icon="🎤"),
    st.Page("pages/5_About_Project.py", title="About Project", icon="ℹ️"),
]
navigation = st.navigation(pages)

with st.sidebar:
    st.divider()
    st.caption("Status")
    st.write(f"{'✅' if st.session_state.get('resume') else '⬜'} Resume uploaded")
    st.write(f"{'✅' if st.session_state.get('job') else '⬜'} Job description analyzed")
    st.write(f"{'🤖 AI on' if ui.get_ai().available else '🧰 Offline mode (no API key)'}")
    if st.session_state.get("resume") or st.session_state.get("job"):
        if st.button("🗑️ Clear all data", width="stretch"):
            for key in ("resume", "resume_file_id", "job", "jd_text"):
                st.session_state.pop(key, None)
            ui.init_state()
            ui.reset_derived()
            st.rerun()

navigation.run()
