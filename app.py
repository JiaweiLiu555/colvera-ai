"""Colvera product demonstration and separate research-archive entry point.

The default screen is deliberately a synthetic, non-clinical product demo.  The
research implementation and saved v0.1/v0.2 artifacts are preserved behind the
Research archive control so the two evidence contexts are never conflated.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from colvera.demo.patient import DemoPatient, DemoVisit, get_demo_patient, get_demo_patients
from colvera.demo.visuals import exam_visual, trend_chart


st.set_page_config(page_title="Colvera", page_icon="C", layout="wide", initial_sidebar_state="collapsed")
LOGO_PATH = ROOT / "assets" / "colvera-ai-logo.png"


def inject_design_system() -> None:
    """Apply the product's shared visual system without changing the backend."""
    st.markdown(
        """
        <style>
        :root {
          --navy: #101b4d;
          --ink: #162347;
          --muted: #596887;
          --line: #dce5f2;
          --paper: #f8faff;
          --card: #ffffff;
          --soft: #f0f5fb;
          --cyan: #1dbbd7;
          --teal: #119b9b;
          --teal-dark: #08777c;
          --violet: #7054d9;
          --violet-dark: #5138b6;
          --violet-soft: #f0edff;
          --cyan-soft: #eaf9fc;
          --amber: #9a6925;
          --amber-soft: #fff5e5;
          --success: #177d72;
          --success-soft: #e8f7f3;
          --shadow-xs: 0 1px 2px rgba(20, 34, 71, .04);
          --shadow: 0 10px 28px rgba(24, 44, 89, .08);
          --radius: 16px;
        }
        #MainMenu, footer, header { visibility: hidden; }
        .stApp { background: radial-gradient(circle at 88% -6%, rgba(112,84,217,.09), transparent 23rem), radial-gradient(circle at 7% 0%, rgba(29,187,215,.075), transparent 27rem), var(--paper); color: var(--ink); }
        .block-container { max-width: 1400px; padding: 1.35rem 3.1rem 4.2rem; }
        @media (max-width: 900px) { .block-container { padding: 1.05rem 1.05rem 2.6rem; } }
        h1, h2, h3, p, div, span { font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
        h1 { color: var(--ink); letter-spacing: -.048em; font-size: 2.25rem !important; line-height: 1.08; }
        h2, h3 { color: var(--ink); letter-spacing: -.028em; }
        [data-testid="stHorizontalBlock"] { align-items: stretch; gap: 1rem; }
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] { min-width: 0; }
        [data-testid="stVerticalBlockBorderWrapper"] { border: 1px solid var(--line); border-radius: var(--radius); background: var(--card); }
        div[data-testid="stMetric"] { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 14px 16px; box-shadow: var(--shadow-xs); }
        [data-testid="stMetricLabel"] { color: var(--muted); font-size: .72rem; text-transform: uppercase; letter-spacing: .08em; }
        [data-testid="stMetricValue"] { color: var(--ink); font-size: 1.2rem; }
        .stButton > button { border-radius: 11px; border: 1px solid #c7d5e8; color: var(--navy); background: rgba(255,255,255,.92); box-shadow: var(--shadow-xs); font-weight: 690; min-height: 42px; transition: background .15s ease, border-color .15s ease, transform .15s ease; }
        .stButton > button:hover { border-color: var(--cyan); color: var(--navy); background: #f5fbff; transform: translateY(-1px); }
        .stButton > button[kind="primary"] { border-color: transparent; background: linear-gradient(110deg, var(--navy), var(--violet)); color: white; box-shadow: 0 8px 18px rgba(81,56,182,.18); }
        .stButton > button[kind="primary"]:hover { border-color: transparent; background: linear-gradient(110deg, #172765, #6043d2); color: white; }
        .stButton > button:disabled { color: #8290a8; border-color: #dce4ef; background: #f3f6fa; opacity: 1; }
        .stRadio [role="radiogroup"] { gap: .22rem; padding: .22rem; background: #eef3fa; border: 1px solid var(--line); border-radius: 12px; width: fit-content; }
        .stRadio [role="radiogroup"] label { margin:0; padding:.42rem .78rem; border-radius:8px; color:#354b70 !important; font-size:.83rem; font-weight:720; white-space:nowrap; opacity:1 !important; }
        .stRadio [role="radiogroup"] label p { margin:0; padding:0; color:#354b70 !important; font-size:inherit; font-weight:inherit; opacity:1 !important; }
        .stRadio [role="radiogroup"] label:has(input:checked) { background:#fff; color:var(--navy) !important; font-weight:780; box-shadow:0 1px 4px rgba(30,49,93,.12); }
        .stRadio [role="radiogroup"] label:has(input:checked) p { color:var(--navy) !important; font-weight:780; }
        .stRadio [role="radiogroup"] [data-testid="stRadioOption"] > div > div > div:first-child { display: none; }
        [data-testid="stAlert"] { border-radius: 13px; }
        .wordmark { display:flex; align-items:center; gap:10px; padding: .3rem 0 .9rem; min-height: 43px; }
        .brand-mark { width:29px; height:29px; position:relative; flex:0 0 auto; border-radius:10px; background:linear-gradient(135deg, var(--cyan) 0%, var(--teal) 37%, var(--violet) 73%, #a55adb 100%); box-shadow:0 5px 12px rgba(81,56,182,.16); }
        .brand-mark:before { content:""; position:absolute; inset:6px; border-radius:7px 10px 7px 10px; border:1.5px solid rgba(255,255,255,.92); }
        .brand-mark:after { content:""; position:absolute; width:8px; height:8px; right:-2px; top:-2px; border-radius:50%; background:#b9f5ef; border:2px solid white; }
        .wordmark-name { font-size: 1.02rem; letter-spacing: .14em; font-weight: 800; color: var(--navy); }
        .wordmark-rule { width: 1px; height: 17px; background: #cbd6e7; }
        .wordmark-sub { font-size: .7rem; letter-spacing: .07em; text-transform: uppercase; color: var(--muted); }
        .logo-context { display:flex; flex-direction:column; justify-content:center; min-height:64px; padding-left:.15rem; }
        .logo-context strong { color:var(--navy); font-size:.79rem; letter-spacing:.105em; text-transform:uppercase; }
        .logo-context span { color:var(--muted); font-size:.74rem; line-height:1.42; margin-top:.2rem; max-width:310px; }
        .demo-chip { display:inline-flex; align-items:center; border: 1px solid #cfe5ed; background:#f2fbfd; color:#257082; border-radius:999px; padding: .38rem .68rem; font-size: .72rem; font-weight: 700; white-space: nowrap; }
        .eyebrow, .archive-kicker { color: var(--violet-dark); font-size: .68rem; font-weight: 800; letter-spacing: .13em; text-transform: uppercase; }
        .quiet { color: var(--muted); font-size: .9rem; line-height: 1.6; }
        .landing-hero { padding: 3.35rem 0 2.25rem; max-width: 760px; }
        .landing-hero h1 { font-size: 3.55rem !important; max-width: 700px; margin: .42rem 0 .75rem; }
        .landing-hero p { color: var(--muted); line-height: 1.62; font-size: 1.03rem; max-width: 650px; }
        .hero-sidecard { margin-top:3.35rem; border:1px solid #d6e2f2; border-radius:var(--radius); padding:1.1rem 1.18rem; background:linear-gradient(145deg,rgba(255,255,255,.92),rgba(240,248,254,.92)); box-shadow:var(--shadow); }
        .hero-sidecard .eyebrow { margin-bottom:.68rem; }
        .hero-queue { display:flex; align-items:baseline; gap:.55rem; }
        .hero-queue strong { color:var(--navy); font-size:2.45rem; letter-spacing:-.07em; line-height:1; }
        .hero-queue span { color:#425b80; font-size:.82rem; font-weight:730; }
        .hero-divider { height:1px; background:#dde7f4; margin:.95rem 0 .8rem; }
        .hero-sidecard p { color:var(--muted); font-size:.8rem; line-height:1.5; margin:0; }
        .hero-statusline { display:flex; align-items:center; gap:.42rem; color:#397067; font-size:.75rem; font-weight:720; margin-top:.78rem; }
        .hero-statusline:before { content:""; width:8px; height:8px; border-radius:50%; background:var(--teal); box-shadow:0 0 0 4px rgba(17,155,155,.11); }
        .review-header { display:flex; align-items:end; justify-content:space-between; gap:1rem; margin: 1.15rem 0 .85rem; }
        .review-header h2 { margin:0; font-size:1.28rem; }
        .review-count { color:var(--muted); font-size:.81rem; text-align:right; }
        .review-card { position:relative; overflow:hidden; border:1px solid var(--line); border-radius:var(--radius); padding: 1.3rem 1.3rem; min-height: 148px; background:var(--card); box-shadow: var(--shadow-xs); }
        .review-card.primary { border-color:#c7d9ef; background:linear-gradient(135deg, #f4faff, #ffffff 62%); box-shadow:var(--shadow); }
        .review-card.primary:before { content:""; position:absolute; top:0; left:0; right:0; height:3px; background:linear-gradient(90deg,var(--cyan),var(--teal),var(--violet)); }
        .review-patient { font-size:1.18rem; font-weight:760; letter-spacing:-.025em; color:var(--ink); margin-bottom:.32rem; }
        .review-meta { color:var(--muted); font-size:.82rem; line-height:1.4; margin-bottom: 1rem; }
        .status { display:inline-flex; align-items:center; gap:.42rem; border-radius:999px; padding:.32rem .62rem; font-size:.73rem; font-weight:720; }
        .status:before { content:""; width:6px; height:6px; border-radius:50%; background:currentColor; }
        .status.review { color:#5d42b9; background:var(--violet-soft); }
        .status.stable { color:var(--success); background:var(--success-soft); }
        .workspace-head { padding: 1rem 0 1.2rem; border-bottom:1px solid var(--line); margin-bottom: 1.25rem; }
        .patient-title { display:flex; gap: 12px; align-items:center; flex-wrap:wrap; margin-bottom:.68rem; }
        .patient-title h1 { font-size: 2.02rem !important; margin:0; }
        .pathway-chip { background:var(--cyan-soft); color:var(--teal-dark); border:1px solid #cfeaf0; border-radius:999px; padding:.32rem .64rem; font-size:.73rem; font-weight:720; }
        .patient-details { display:flex; flex-wrap:wrap; gap: .46rem 1.2rem; color:var(--muted); font-size:.84rem; line-height:1.45; }
        .patient-details strong { color:#324568; font-weight:700; }
        .assessment { position:relative; overflow:hidden; border:1px solid #cfdcf3; border-radius:var(--radius); padding:1.5rem 1.6rem; background:linear-gradient(116deg,#eef9fc 0%, #f7f4ff 56%, #ffffff 100%); box-shadow:var(--shadow); }
        .assessment:after { content:""; position:absolute; width:230px; height:230px; right:-80px; bottom:-130px; border-radius:50%; background:radial-gradient(circle, rgba(112,84,217,.17), rgba(112,84,217,0) 68%); pointer-events:none; }
        .assessment h2 { position:relative; font-size:1.55rem; margin: .4rem 0 .5rem; max-width:680px; }
        .assessment p { position:relative; color:#485b7b; font-size:.93rem; line-height:1.58; margin:0; max-width:700px; }
        .assessment .assessment-foot { position:relative; display:flex; gap:.52rem; align-items:center; margin-top:1rem; color:#315674; font-size:.8rem; font-weight:720; }
        .assessment .assessment-foot:before { content:""; width:8px; height:8px; border-radius:50%; background:var(--violet); box-shadow:0 0 0 4px rgba(112,84,217,.12); }
        .assessment.stable { border-color:#c7e7df; background:linear-gradient(116deg,#edfbf8 0%,#f1f9fd 56%,#ffffff 100%); }
        .assessment.stable:after { background:radial-gradient(circle, rgba(17,155,155,.16), rgba(17,155,155,0) 68%); }
        .assessment.stable .assessment-foot { color:#236d68; }
        .assessment.stable .assessment-foot:before { background:var(--teal); box-shadow:0 0 0 4px rgba(17,155,155,.12); }
        .assessment-chips { position:relative; display:flex; flex-wrap:wrap; gap:.45rem; margin-top:1rem; }
        .assessment-chips span { border:1px solid #d3def1; border-radius:999px; background:rgba(255,255,255,.68); color:#486080; padding:.27rem .54rem; font-size:.72rem; font-weight:700; }
        .mini-heading { margin: .5rem 0 .7rem; display:flex; justify-content:space-between; align-items:baseline; gap:1rem; }
        .mini-heading h3 { margin:0; font-size: .78rem; color:#455a80; letter-spacing:.115em; text-transform:uppercase; }
        .mini-heading span { color:var(--muted); font-size:.77rem; text-align:right; }
        .timeline-caption { margin-top:.7rem; color:#63728f; font-size:.82rem; }
        .selected-visit { padding: .9rem 1rem; margin-top:.82rem; border-left:3px solid var(--cyan); background:#f1f8fd; border-radius:0 12px 12px 0; color:#395474; font-size:.86rem; line-height:1.52; }
        .change-card { height:100%; min-height:158px; border:1px solid var(--line); background:var(--card); border-radius:14px; padding: 1.02rem 1.05rem; box-shadow:var(--shadow-xs); }
        .change-card h4 { margin:0 0 .7rem; color:var(--ink); font-size:.93rem; }
        .change-card .previous { color:var(--muted); font-size:.8rem; line-height:1.45; }
        .change-card .current { color:#344b70; font-size:.82rem; line-height:1.45; margin-top:.42rem; font-weight:660; }
        .change-arrow { color:var(--violet-dark); font-size:.74rem; font-weight:780; margin-top:.85rem; }
        .change-arrow.monitor { color:var(--amber); }
        .change-arrow.stable { color:var(--success); }
        .concordance { display:flex; align-items:center; gap:10px; padding: 1rem 1.15rem; border-radius:14px; background:linear-gradient(108deg,var(--navy),#263b81 56%,var(--violet-dark)); color:#f7f9ff; margin-top:.9rem; box-shadow:0 8px 18px rgba(36,52,113,.15); }
        .concordance .dot { height:9px; width:9px; border-radius:50%; background:#67e0df; box-shadow:0 0 0 4px rgba(103,224,223,.14); flex:0 0 auto; }
        .concordance p { margin:0; font-size:.86rem; line-height:1.5; }
        .section-intro { color:var(--muted); max-width:760px; line-height:1.6; margin: .24rem 0 0; font-size:.94rem; }
        .exam-panel { border:1px solid var(--line); border-radius:var(--radius); padding: 1rem; background:var(--card); height:100%; box-shadow:var(--shadow-xs); }
        .exam-panel.current { border-color:#d7ccef; background:linear-gradient(145deg,#fff,#fbfaff); box-shadow:0 10px 24px rgba(112,84,217,.08); }
        .exam-label { color:var(--muted); font-size:.68rem; letter-spacing:.105em; text-transform:uppercase; font-weight:760; }
        .exam-date { color:var(--ink); font-size:1.04rem; font-weight:760; margin:.25rem 0 .56rem; }
        .exam-note { color:#506482; font-size:.83rem; line-height:1.46; min-height:40px; margin:.72rem 0 .15rem; }
        .exam-visual { margin-top:.78rem; }
        .exam-visual svg { width:100%; height:auto; display:block; border-radius:12px; }
        .exam-visual-caption { color:var(--muted); display:flex; justify-content:space-between; font-size:.71rem; padding:.48rem .12rem 0; }
        .evidence-card { border: 1px solid var(--line); background:var(--card); border-radius:14px; padding:1.02rem; min-height:130px; height:100%; box-shadow:var(--shadow-xs); }
        .evidence-name { display:flex; align-items:center; justify-content:space-between; gap:.55rem; font-size:.91rem; font-weight:760; color:var(--ink); }
        .evidence-copy { font-size:.82rem; color:var(--muted); line-height:1.47; min-height:49px; margin:.6rem 0 .74rem; }
        .evidence-tag { font-size:.7rem; color:#5a40b8; background:var(--violet-soft); border-radius:999px; padding:.27rem .45rem; font-weight:750; white-space:nowrap; }
        .evidence-tag.stable { color:var(--success); background:var(--success-soft); }
        .summary-card { position:relative; overflow:hidden; background:linear-gradient(145deg,var(--navy),#263c87 58%,var(--violet-dark)); color:white; border-radius:var(--radius); padding:1.35rem 1.38rem; height:100%; box-shadow:0 13px 28px rgba(26,39,99,.19); }
        .summary-card:after { content:""; position:absolute; width:180px; height:180px; border:1px solid rgba(116,230,228,.18); border-radius:50%; right:-72px; bottom:-76px; }
        .summary-card h3 { position:relative; color:#fff; font-size:.79rem; letter-spacing:.12em; text-transform:uppercase; margin:0 0 .72rem; }
        .summary-card p { position:relative; color:#e8edff; line-height:1.56; font-size:.86rem; margin:.35rem 0 .92rem; }
        .summary-card ul { position:relative; margin:.25rem 0 1rem; padding-left:1.12rem; color:#f5f7ff; font-size:.81rem; line-height:1.7; }
        .summary-action { position:relative; border-top:1px solid rgba(255,255,255,.18); padding-top:.78rem; color:#bcf4ed; font-size:.8rem; line-height:1.46; }
        .trajectory { display:flex; align-items:center; gap:.9rem; border:1px solid var(--line); border-radius:13px; padding:.85rem .9rem; margin-bottom:.6rem; background:var(--card); box-shadow:var(--shadow-xs); }
        .trajectory-index { color:var(--violet-dark); font-size:.73rem; font-weight:800; background:var(--violet-soft); width:28px; height:28px; border-radius:9px; display:grid; place-items:center; flex:0 0 auto; }
        .trajectory-main { flex:1; min-width:0; }
        .trajectory-main strong { display:block; color:var(--ink); font-size:.83rem; }
        .trajectory-main span { color:var(--muted); font-size:.77rem; line-height:1.4; }
        .trajectory-score { color:#5d42b9; font-weight:750; font-size:.74rem; white-space:nowrap; }
        .trend-panel { border:1px solid var(--line); border-radius:14px; padding:1rem .98rem .62rem; background:var(--card); box-shadow:var(--shadow-xs); }
        .trend-title { display:flex; align-items:baseline; justify-content:space-between; gap:.5rem; color:#526687; font-size:.81rem; }
        .trend-title span { font-weight:750; color:#34496e; }
        .trend-title strong { color:#657493; font-size:.72rem; font-weight:720; white-space:nowrap; }
        .trend-svg { width:100%; height:auto; display:block; margin-top:.2rem; }
        .footer-note { color:#6d7b95; border-top:1px solid var(--line); padding-top:1rem; margin-top:2.25rem; font-size:.74rem; line-height:1.5; }
        .archive-kicker { margin-top:1.5rem; }
        .archive-notice { display:flex; align-items:flex-start; gap:.75rem; border:1px solid #c8bff2; border-radius:14px; padding:.9rem 1rem; margin:.85rem 0 1.25rem; background:linear-gradient(105deg,#f4f2ff,#edfbfb); color:#26355f; font-size:.88rem; line-height:1.5; }
        .archive-notice:before { content:"i"; width:20px; height:20px; border-radius:50%; display:grid; place-items:center; flex:0 0 auto; background:linear-gradient(135deg,var(--violet),var(--teal)); color:white; font-weight:800; font-size:.76rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def top_bar() -> None:
    brand, actions = st.columns([5, 2])
    with brand:
        logo, context = st.columns([1.5, 3.2])
        with logo:
            st.image(str(LOGO_PATH), width=188)
        with context:
            st.markdown(
                "<div class='logo-context'><strong>Longitudinal cancer intelligence</strong>"
                "<span>AI-assisted surveillance for clinician review</span></div>",
                unsafe_allow_html=True,
            )
    with actions:
        right, archive = st.columns([1.25, 1])
        with right:
            st.markdown("<div style='padding-top:.42rem; text-align:right'><span class='demo-chip'>Demo patient · Synthetic data</span></div>", unsafe_allow_html=True)
        with archive:
            if st.button("Research archive", key="open_archive", use_container_width=True):
                st.session_state["screen"] = "archive"
                st.rerun()


def card(title: str, previous: str, current: str, status: str, tone: str = "") -> str:
    return f"""
    <div class='change-card'>
      <h4>{title}</h4>
      <div class='previous'><strong>Previous</strong> · {previous}</div>
      <div class='current'><strong>Current</strong> · {current}</div>
      <div class='change-arrow {tone}'>→ {status}</div>
    </div>
    """


def evidence_card(name: str, description: str, tag: str, stable: bool = False) -> str:
    tone = " stable" if stable else ""
    return f"""
    <div class='evidence-card'>
      <div class='evidence-name'><span>{name}</span><span class='evidence-tag{tone}'>{tag}</span></div>
      <div class='evidence-copy'>{description}</div>
    </div>
    """


def render_landing() -> None:
    top_bar()
    hero, snapshot = st.columns([1.42, .68])
    with hero:
        st.markdown(
            """
            <div class='landing-hero'>
              <div class='eyebrow'>Longitudinal · Multimodal · Comparative</div>
              <h1>Surveillance, understood in context.</h1>
              <p>Colvera brings a patient's serial MRI, endoscopy, and clinical evidence into one AI-assisted surveillance assessment—centered on what has changed from their own prior examination.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with snapshot:
        st.markdown(
            """
            <div class='hero-sidecard'>
              <div class='eyebrow'>Today's queue</div>
              <div class='hero-queue'><strong>3</strong><span>synthetic reviews scheduled</span></div>
              <div class='hero-divider'></div>
              <p>One review shows a new longitudinal change; two demonstrate stable surveillance patterns.</p>
              <div class='hero-statusline'>Demo environment · no patient data</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<div class='review-header'><h2>Today's surveillance reviews</h2><span class='review-count'>3 scheduled reviews · demonstration workspace</span></div>", unsafe_allow_html=True)
    for index, (column, patient) in enumerate(zip(st.columns(3), get_demo_patients())):
        with column:
            card_class = " primary" if index == 0 else ""
            status_class = "review" if patient.has_interval_change else "stable"
            status_copy = "New longitudinal change · Review recommended" if patient.has_interval_change else "Stable surveillance pattern"
            st.markdown(
                f"<div class='review-card{card_class}'><div class='review-patient'>Patient {patient.patient_id}</div>"
                f"<div class='review-meta'>{patient.pathway} · Current examination</div>"
                f"<span class='status {status_class}'>{status_copy}</span></div>",
                unsafe_allow_html=True,
            )
            label = "Open patient workspace" if index == 0 else "Open stable review"
            if st.button(label, key=f"open_patient_{patient.patient_id}", type="primary" if index == 0 else "secondary", use_container_width=True):
                st.session_state["selected_patient_id"] = patient.patient_id
                st.session_state["screen"] = "workspace"
                st.rerun()
    st.markdown(
        "<div class='footer-note'>Colvera is a product demonstration using synthetic patient data. It is not a diagnostic device, has not been clinically validated, and does not replace professional review.</div>",
        unsafe_allow_html=True,
    )


def render_patient_header(patient: DemoPatient) -> None:
    st.markdown(
        f"""
        <div class='workspace-head'>
          <div class='patient-title'><h1>Patient {patient.patient_id}</h1><span class='pathway-chip'>{patient.pathway}</span></div>
          <div class='patient-details'>
            <span><strong>{patient.age_range}</strong> · {patient.sex}</span><span>{patient.treatment_history}</span>
            <span><strong>{patient.surveillance_duration}</strong> in surveillance</span><span>Last visit <strong>{patient.last_visit}</strong></span><span>Next follow-up <strong>{patient.next_follow_up}</strong></span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_assessment(patient: DemoPatient) -> None:
    if patient.has_interval_change:
        headline = "Increased concern compared with previous examination"
        description = "New concordant changes are present on MRI and endoscopy compared with the patient's July examination. This AI-assisted surveillance assessment is intended to support, not replace, clinician review."
        chips = "<span>New interval change</span><span>Two corroborating sources</span><span>Professional review required</span>"
        foot = "MRI and endoscopy show interval change in the same surveillance visit"
        state_class = ""
    else:
        headline = "Stable surveillance pattern compared with previous examination"
        description = "MRI, endoscopy, clinical examination, and CEA remain without a clearly new interval finding compared with the patient's July examination. This AI-assisted surveillance assessment is intended to support, not replace, clinician review."
        chips = "<span>No new focal change</span><span>Multimodal stability</span><span>Routine review continues</span>"
        foot = "No new concerning interval change is illustrated in this synthetic visit"
        state_class = " stable"
    st.markdown(
        f"""
        <div class='assessment{state_class}'>
          <div class='eyebrow'>Current surveillance assessment</div>
          <h2>{headline}</h2>
          <p>{description}</p>
          <div class='assessment-chips'>{chips}</div>
          <div class='assessment-foot'>{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_timeline_selector(patient: DemoPatient) -> DemoVisit:
    st.markdown("<div class='mini-heading'><h3>Surveillance timeline</h3><span>Select a visit to inspect its evidence</span></div>", unsafe_allow_html=True)
    labels = [visit.short_date for visit in patient.visits]
    selected = st.radio("Surveillance visit", labels, horizontal=True, key="visit_selector", label_visibility="collapsed", index=len(labels) - 1)
    visit = next(item for item in patient.visits if item.short_date == selected)
    roles = " · ".join(f"<strong>{item.short_date}</strong> — {item.role}" for item in patient.visits)
    st.markdown(f"<div class='timeline-caption'>{roles}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='selected-visit'><strong>{visit.short_date} · {visit.role}</strong> &nbsp; MRI: {visit.mri} &nbsp; Endoscopy: {visit.endoscopy} &nbsp; CEA: {visit.cea:.1f} ng/mL</div>",
        unsafe_allow_html=True,
    )
    return visit


def render_change_since_previous(patient: DemoPatient) -> None:
    previous, current = patient.previous_visit, patient.current_visit
    if patient.has_interval_change:
        imaging_status, imaging_tone = "Increased concern", ""
        cea_status, cea_tone = "Mild increase", "monitor"
        synthesis = "Two modalities demonstrate new concordant change since the previous surveillance visit."
    else:
        imaging_status, imaging_tone = "No material change", "stable"
        cea_status, cea_tone = "Stable range", "stable"
        synthesis = "The reviewed surveillance sources remain stable relative to the previous synthetic visit."
    st.markdown("<div class='mini-heading'><h3>Change since previous exam</h3><span>July 2026 → August 2026</span></div>", unsafe_allow_html=True)
    one, two, three, four = st.columns(4)
    with one:
        st.markdown(card("MRI", previous.mri, current.mri, imaging_status, imaging_tone), unsafe_allow_html=True)
    with two:
        st.markdown(card("Endoscopy", previous.endoscopy, current.endoscopy, imaging_status, imaging_tone), unsafe_allow_html=True)
    with three:
        st.markdown(card("CEA", f"{previous.cea:.1f} ng/mL", f"{current.cea:.1f} ng/mL", cea_status, cea_tone), unsafe_allow_html=True)
    with four:
        st.markdown(card("Clinical / DRE", previous.dre, current.dre, "Stable", "stable"), unsafe_allow_html=True)
    st.markdown(
        f"<div class='concordance'><span class='dot'></span><p><strong>Multimodal synthesis</strong> &nbsp; {synthesis}</p></div>",
        unsafe_allow_html=True,
    )


def trends(patient: DemoPatient) -> None:
    st.markdown("<div class='mini-heading'><h3>Longitudinal trends</h3><span>Visual aids within this synthetic demonstration</span></div>", unsafe_allow_html=True)
    one, two = st.columns(2)
    with one:
        st.markdown(trend_chart("CEA across surveillance visits", tuple(item.short_date for item in patient.visits), tuple(item.cea for item in patient.visits), "#119B9B", "ng/mL"), unsafe_allow_html=True)
    with two:
        st.markdown(trend_chart("Imaging change score", tuple(item.short_date for item in patient.visits), tuple(float(item.imaging_change_score) for item in patient.visits), "#7054D9", "relative"), unsafe_allow_html=True)


def render_overview(patient: DemoPatient) -> None:
    render_assessment(patient)
    render_timeline_selector(patient)
    render_change_since_previous(patient)
    trends(patient)


def render_timeline(patient: DemoPatient) -> None:
    timeline_copy = "Each visit is read in sequence so that a current examination is interpreted against this patient's own prior pattern—not in isolation."
    title = "The patient is the reference." if patient.has_interval_change else "A stable pattern, seen over time."
    st.markdown(f"<div class='eyebrow'>Longitudinal</div><h2 style='margin:.32rem 0 .2rem'>{title}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p class='section-intro'>{timeline_copy}</p>", unsafe_allow_html=True)
    render_timeline_selector(patient)
    trends(patient)
    st.markdown("<div class='mini-heading'><h3>Current comparison</h3><span>Latest completed interval</span></div>", unsafe_allow_html=True)
    render_change_since_previous(patient)


def render_compare(patient: DemoPatient) -> None:
    st.markdown("<div class='eyebrow'>Comparative</div><h2 style='margin:.32rem 0 .2rem'>Compare examinations directly.</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-intro'>Synthetic imaging-style illustrations make the prior/current workflow tangible. They are not diagnostic images or model outputs.</p>", unsafe_allow_html=True)
    controls, overlay_column = st.columns([2.1, 1])
    with controls:
        modality = st.radio("Comparison modality", ["MRI", "Endoscopy"], horizontal=True, key="comparison_modality", label_visibility="collapsed")
    with overlay_column:
        overlay_state = st.radio("Change overlay", ["Overlay on", "Overlay off"], horizontal=True, key="show_overlay", label_visibility="collapsed")
        show_overlay = overlay_state == "Overlay on"
    previous, current = patient.previous_visit, patient.current_visit
    left, right = st.columns(2)
    with left:
        previous_note = previous.mri if modality == "MRI" else previous.endoscopy
        st.markdown(f"<div class='exam-panel'><div class='exam-label'>Previous exam</div><div class='exam-date'>{previous.short_date}</div><div class='exam-note'>{previous_note}</div>{exam_visual(previous, modality, False)}</div>", unsafe_allow_html=True)
    with right:
        current_note = current.mri if modality == "MRI" else current.endoscopy
        st.markdown(f"<div class='exam-panel current'><div class='exam-label'>Current exam</div><div class='exam-date'>{current.short_date}</div><div class='exam-note'>{current_note}</div>{exam_visual(current, modality, show_overlay and patient.has_interval_change)}</div>", unsafe_allow_html=True)
    if patient.has_interval_change:
        evidence_label = "focal signal change" if modality == "MRI" else "focal scar-margin irregularity"
        observation = f"The current {modality} illustration marks a new {evidence_label} relative to July. Clinical review should consider this alongside the full examination and other evidence."
    else:
        observation = f"The current {modality} illustration shows no new focal interval change relative to July in this synthetic case. Clinical review should continue to consider the full examination and other evidence."
    st.markdown(f"<div class='concordance'><span class='dot'></span><p><strong>Comparison observation</strong> &nbsp; {observation}</p></div>", unsafe_allow_html=True)


def render_evidence(patient: DemoPatient) -> None:
    st.markdown("<div class='eyebrow'>Multimodal</div><h2 style='margin:.32rem 0 .2rem'>Evidence, brought together.</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-intro'>Colvera organizes evidence from multiple surveillance sources so a reviewer can see what changed, what remained stable, and where the sources agree.</p>", unsafe_allow_html=True)
    previous, current = patient.previous_visit, patient.current_visit
    if patient.has_interval_change:
        card_data = [
            ("MRI", "New focal interval signal change at the treated tumor bed compared with July.", "Concern ↑", False),
            ("Endoscopy", "New focal superficial irregularity at the scar margin compared with July.", "Concern ↑", False),
            ("CEA", f"Mild upward change from {previous.cea:.1f} to {current.cea:.1f} ng/mL across the latest interval.", "Monitor", False),
            ("Clinical / DRE", "No major interval change documented at the current surveillance visit.", "Stable", True),
        ]
        trajectories = [
            ("01", "High similarity", "Stable → subtle multimodal change → subsequent regrowth review pathway", "Illustrative"),
            ("02", "Moderate similarity", "Temporary MRI change → subsequent examination resolved", "Illustrative"),
            ("03", "Moderate similarity", "Isolated CEA increase → subsequent surveillance remained stable", "Illustrative"),
        ]
        summary_text = (
            "Compared with the July 2026 surveillance examination, the current visit demonstrates new concordant changes on MRI and endoscopy, accompanied by a mild increase in CEA. "
            "These findings represent an interval change in the patient's surveillance pattern."
        )
        summary_items = "<li>New MRI finding</li><li>New endoscopic irregularity</li><li>CEA increased from 2.1 → 3.0</li>"
        suggested_action = "Review current examination alongside prior studies."
    else:
        card_data = [
            ("MRI", "Current treated tumor bed remains stable without a new focal signal change.", "Stable", True),
            ("Endoscopy", "Current scar appearance remains stable without a new irregularity.", "Stable", True),
            ("CEA", f"CEA remains within the illustrated surveillance range: {previous.cea:.1f} → {current.cea:.1f} ng/mL.", "Stable", True),
            ("Clinical / DRE", "No major interval change documented at the current surveillance visit.", "Stable", True),
        ]
        trajectories = [
            ("01", "High similarity", "Stable MRI and endoscopy across sequential surveillance visits", "Illustrative"),
            ("02", "Moderate similarity", "Minor biomarker variation → subsequent surveillance remained stable", "Illustrative"),
            ("03", "Moderate similarity", "Stable scar appearance → routine surveillance continued", "Illustrative"),
        ]
        summary_text = (
            "Compared with the July 2026 surveillance examination, the current visit remains without a clearly new focal MRI or endoscopic change in this synthetic case. "
            "The available surveillance sources illustrate a stable pattern over the latest interval."
        )
        summary_items = "<li>No new focal MRI change</li><li>Stable endoscopic scar appearance</li><li>CEA remains in the illustrated range</li>"
        suggested_action = "Continue routine professional surveillance review."
    cards = st.columns(4)
    for column, values in zip(cards, card_data):
        with column:
            st.markdown(evidence_card(*values), unsafe_allow_html=True)
    content, summary = st.columns([1.45, 1])
    with content:
        st.markdown("<div class='mini-heading'><h3>Similar surveillance trajectories</h3><span>Demonstration trajectories · synthetic</span></div>", unsafe_allow_html=True)
        for index, title, description, score in trajectories:
            st.markdown(f"<div class='trajectory'><span class='trajectory-index'>{index}</span><div class='trajectory-main'><strong>{title}</strong><span>{description}</span></div><span class='trajectory-score'>{score}</span></div>", unsafe_allow_html=True)
        st.caption("Illustrative synthetic trajectories only. They do not represent a trained similarity model or clinical outcome evidence.")
    with summary:
        st.markdown(
            f"""
            <div class='summary-card'>
              <h3>Colvera summary</h3>
              <p>{summary_text}</p>
              <ul>{summary_items}</ul>
              <div class='summary-action'><strong>Suggested action</strong><br>{suggested_action}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_workspace(patient: DemoPatient) -> None:
    top_bar()
    if st.button("← Today’s reviews", key="back_to_reviews"):
        st.session_state["screen"] = "reviews"
        st.rerun()
    render_patient_header(patient)
    section = st.radio("Workspace navigation", ["Overview", "Timeline", "Compare exams", "Evidence"], horizontal=True, key="workspace_navigation", label_visibility="collapsed")
    if section == "Overview":
        render_overview(patient)
    elif section == "Timeline":
        render_timeline(patient)
    elif section == "Compare exams":
        render_compare(patient)
    else:
        render_evidence(patient)
    st.markdown(
        "<div class='footer-note'>Demo patient · Synthetic data. Colvera presents an AI-assisted surveillance assessment for professional review; it does not diagnose cancer, rule out cancer, or replace professional examination.</div>",
        unsafe_allow_html=True,
    )


def main() -> None:
    inject_design_system()
    st.session_state.setdefault("screen", "reviews")
    st.session_state.setdefault("selected_patient_id", "024")
    if st.session_state["screen"] == "archive":
        from colvera.research_archive import render_research_archive

        top_bar()
        if st.button("← Back to product demo", key="back_from_archive"):
            st.session_state["screen"] = "reviews"
            st.rerun()
        render_research_archive(ROOT)
        return
    if st.session_state["screen"] == "workspace":
        render_workspace(get_demo_patient(st.session_state["selected_patient_id"]))
    else:
        render_landing()


if __name__ == "__main__":
    main()
