import streamlit as st
import joblib
import pandas as pd
import os
import time

# ─────────────────────────────────────────────
# 1.  PAGE CONFIG & STATE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="R&Y Credit Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

# ─────────────────────────────────────────────
# 2.  DYNAMIC CSS & ELEGANT STYLING
# ─────────────────────────────────────────────
if st.session_state.theme == "dark":
    theme_vars = """
    :root {
        --bg-main: #0f1923;
        --bg-card: #1c2d42;
        --text-main: #f4f0e8;
        --text-muted: #8a9bae;
        --gold: #c9a84c;
        --gold-light: #e8c97a;
        --border: rgba(201,168,76,0.2);
        --input-bg: rgba(255,255,255,0.05);
        --shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    """
else:
    theme_vars = """
    :root {
        --bg-main: #f8f9fa;
        --bg-card: #ffffff;
        --text-main: #1a1a1a;
        --text-muted: #555555;
        --gold: #b38f2d;
        --gold-light: #c9a84c;
        --border: rgba(0,0,0,0.12);
        --input-bg: #f4f6f8;
        --shadow: 0 4px 24px rgba(0,0,0,0.06);
    }
    """

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600&display=swap');

{theme_vars}

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    color: var(--text-main);
}}
.stApp {{ background: var(--bg-main); }}

/* Single Screen Padding */
.block-container {{ padding: 1.5rem 2.5rem 1rem !important; max-width: 1400px !important; }}

/* Header */
.ry-header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem; }}
.ry-header-left {{ display: flex; align-items: center; gap: 1rem; }}
.ry-logo {{
    width: 48px; height: 48px;
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold-light) 100%);
    border-radius: 12px; display: flex; align-items: center; justify-content: center;
    font-size: 1.6rem; box-shadow: 0 4px 14px rgba(201,168,76,0.25);
}}
.ry-title h1 {{ font-family: 'Playfair Display', serif; font-size: 1.7rem; margin: 0; color: var(--text-main); font-weight: 700; letter-spacing: -0.5px; }}
.ry-title p {{ color: var(--gold); font-size: 0.75rem; font-weight: 600; text-transform: uppercase; margin: 2px 0 0; letter-spacing: 2px; }}

.gold-line {{ height: 1px; background: linear-gradient(90deg, transparent, var(--gold), transparent); margin: 0.8rem 0 1.2rem 0; opacity: 0.5; }}

/* Cards & Section Headers */
.elegant-card {{
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 1rem 1.5rem; box-shadow: var(--shadow);
    margin-bottom: 1rem;
}}
.section-label {{ font-size: 0.75rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: var(--gold); margin-bottom: 0.5rem; display: flex; align-items: center; }}
.step-badge {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 22px; height: 22px; background: rgba(201,168,76,0.15);
    border: 1px solid rgba(201,168,76,0.3); border-radius: 50%;
    color: var(--gold); font-size: 0.65rem; font-weight: 700; margin-right: 8px;
}}

/* Compact Inputs */
.stSelectbox > div > div, .stNumberInput > div > div > input {{
    background: var(--input-bg) !important; border: 1px solid var(--border) !important;
    color: var(--text-main) !important; font-size: 0.85rem !important;
    border-radius: 6px !important; padding: 0.2rem 0.5rem !important; min-height: 2.2rem !important;
}}
.stSelectbox label, .stNumberInput label {{ color: var(--text-muted) !important; font-size: 0.75rem !important; font-weight: 600 !important; }}

/* Theme Toggle Button */
div[data-testid="stButton"]:has(button[kind="secondary"]) > button {{
    background: transparent !important; color: var(--gold) !important;
    border: 1px solid var(--border) !important; box-shadow: none !important;
    font-size: 0.75rem !important; padding: 0.3rem 0.8rem !important; letter-spacing: 1px;
}}

/* Primary Run Button */
div[data-testid="stButton"]:has(button[kind="primary"]) > button {{
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold-light) 100%) !important;
    color: #0f1923 !important; font-family: 'DM Sans', sans-serif !important; font-weight: 700 !important;
    border: none !important; border-radius: 8px !important; padding: 0.5rem 1rem !important;
    letter-spacing: 1.5px !important; box-shadow: 0 4px 15px rgba(201,168,76,0.3) !important; transition: all 0.2s;
}}
div[data-testid="stButton"]:has(button[kind="primary"]) > button:hover {{ filter: brightness(1.1); transform: translateY(-1px); }}

/* Metrics */
[data-testid="stMetric"] {{
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 10px; padding: 0.5rem 1rem; box-shadow: var(--shadow);
}}
[data-testid="stMetricValue"] {{ color: var(--text-main) !important; font-size: 1.3rem !important; font-family: 'Playfair Display', serif !important; }}
[data-testid="stMetricLabel"] {{ color: var(--text-muted) !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.5px; }}

/* Results */
.result-box {{ border-radius: 10px; padding: 1rem 1.5rem; border: 1px solid; margin-top: 0.5rem; display: flex; align-items: center; gap: 1rem; box-shadow: var(--shadow); }}
.approved {{ background: rgba(46,204,143,0.08); border-color: #2ecc8f; border-left: 4px solid #2ecc8f; }}
.rejected {{ background: rgba(224,92,107,0.08); border-color: #e05c6b; border-left: 4px solid #e05c6b; }}
.result-title {{ margin:0; font-family: 'Playfair Display', serif; font-size: 1.25rem; font-weight: 700; }}
.result-text {{ margin:4px 0 0 0; font-size: 0.85rem; color: var(--text-muted); }}

/* Progress Bar */
.stProgress > div > div > div {{ background: var(--gold) !important; border-radius: 99px !important; }}
.stProgress > div > div {{ background: var(--input-bg) !important; border-radius: 99px !important; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3.  MODEL LOADING
# ─────────────────────────────────────────────
@st.cache_resource
def load_my_model():
    model_path = os.path.join('models', 'loan_model.pkl')
    return joblib.load(model_path)

try:
    model = load_my_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    model_error = str(e)

# ─────────────────────────────────────────────
# 4.  HEADER
# ─────────────────────────────────────────────
col_header, col_theme = st.columns([8, 1])
with col_header:
    st.markdown("""
    <div class="ry-header">
        <div class="ry-header-left">
            <div class="ry-logo">🏦</div>
            <div class="ry-title">
                <h1>R&Y Credit Intelligence</h1>
                <p>Automated Underwriting Engine</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_theme:
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    st.button("🌓 Theme", on_click=toggle_theme, key="theme_btn", type="secondary", use_container_width=True)

st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

if not model_loaded:
    st.error(f"Critical: Model unavailable — {model_error}")
    st.stop()

# ─────────────────────────────────────────────
# 5.  ELEGANT COMPACT INPUTS
# ─────────────────────────────────────────────
st.markdown('<div class="elegant-card">', unsafe_allow_html=True)

st.markdown('<div class="section-label"><span class="step-badge">1</span> Applicant Profile</div>', unsafe_allow_html=True)
r1c1, r1c2, r1c3, r1c4 = st.columns(4)
with r1c1: gender     = st.selectbox("Gender", ["Male", "Female"])
with r1c2: married    = st.selectbox("Marital Status", ["No", "Yes"])
with r1c3: dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
with r1c4: education  = st.selectbox("Education", ["Graduate", "Not Graduate"])

st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label"><span class="step-badge">2</span> Financial Details</div>', unsafe_allow_html=True)
r2c1, r2c2, r2c3, r2c4 = st.columns(4)
with r2c1: self_emp   = st.selectbox("Employment", ["Salaried", "Self-Employed"])
with r2c2: app_income = st.number_input("Applicant Income ($)", value=5000, step=500)
with r2c3: coapp_inc  = st.number_input("Co-app Income ($)", value=0, step=500)
with r2c4: loan_amt   = st.number_input("Loan Amt ($000s)", value=150, step=10)

r3c1, r3c2, r3c3, r3c4 = st.columns(4)
with r3c1: term          = st.number_input("Term (Days)", value=360, step=30)
with r3c2: credit_hist   = st.selectbox("Credit History", ["Clear", "Not Clear"])
with r3c3: property_area = st.selectbox("Location", ["Rural", "Semiurban", "Urban"])
with r3c4: 
    st.markdown("<div style='margin-top: 1.65rem;'></div>", unsafe_allow_html=True)
    run_btn = st.button("⚡ RUN ANALYSIS", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 6.  EXECUTION & RESULTS
# ─────────────────────────────────────────────
if run_btn:
    data = {
        'Gender':            1 if gender == "Male" else 0,
        'Married':           1 if married == "Yes" else 0,
        'Dependents':        3 if dependents == "3+" else int(dependents),
        'Education':         0 if education == "Graduate" else 1,
        'Self_Employed':     1 if self_emp == "Self-Employed" else 0,
        'ApplicantIncome':   app_income,
        'CoapplicantIncome': coapp_inc,
        'LoanAmount':        loan_amt,
        'Loan_Amount_Term':  term,
        'Credit_History':    1.0 if credit_hist == "Clear" else 0.0,
        'Property_Area':     {"Rural": 0, "Semiurban": 1, "Urban": 2}[property_area],
    }
    input_df = pd.DataFrame([data])

    # Elegant Loading Sequence
    ph = st.empty()
    bar = ph.progress(0)
    for label, pct in [("Validating profile...", 30), ("Running risk model...", 60), ("Finalising...", 100)]:
        time.sleep(0.2)
        bar.progress(pct, text=label)
    time.sleep(0.2)
    ph.empty()

    prediction = model.predict(input_df)
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(input_df)[0]
        approve_pct = round(proba[1] * 100, 1)
        reject_pct  = round(proba[0] * 100, 1)
    else:
        approve_pct = 100 if prediction[0] == 1 else 0
        reject_pct  = 100 - approve_pct

    m1, m2, m3, m4 = st.columns(4)
    total_income = app_income + coapp_inc
    dti = round((loan_amt * 1000) / (total_income * 12) * 100, 1) if total_income > 0 else 0
    
    m1.metric("Approval Score", f"{approve_pct}%")
    m2.metric("Default Risk", f"{reject_pct}%")
    m3.metric("Household Inc.", f"${total_income:,}/mo")
    m4.metric("DTI Ratio", f"{dti}%")

    if prediction[0] == 1:
        st.markdown(f"""
        <div class="result-box approved">
            <div>
                <h3 class="result-title" style="color:#2ecc8f;">Approved</h3>
                <p class="result-text">Confidence score of <strong style="color:var(--text-main);">{approve_pct}%</strong>. Risk parameters are well within required thresholds.</p>
            </div>
        </div>""", unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown(f"""
        <div class="result-box rejected">
            <div>
                <h3 class="result-title" style="color:#e05c6b;">Declined</h3>
                <p class="result-text">High default probability detected (<strong style="color:var(--text-main);">{reject_pct}%</strong>). Application falls short of underwriting criteria.</p>
            </div>
        </div>""", unsafe_allow_html=True)