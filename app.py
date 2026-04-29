import streamlit as st
import joblib
import pandas as pd
import os
import time

# ─────────────────────────────────────────────
# 1.  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="R&Y Credit Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",   # sidebar starts closed
)

# ─────────────────────────────────────────────
# 2.  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --navy:       #0f1923;
    --navy-mid:   #162233;
    --navy-card:  #1c2d42;
    --gold:       #c9a84c;
    --gold-light: #e8c97a;
    --ivory:      #f4f0e8;
    --muted:      #8a9bae;
    --success:    #2ecc8f;
    --danger:     #e05c6b;
    --radius:     14px;
    --shadow:     0 8px 32px rgba(0,0,0,0.35);
    --shadow-sm:  0 2px 12px rgba(0,0,0,0.20);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--ivory);
}
.stApp {
    background: linear-gradient(145deg, var(--navy) 0%, #0d1f31 100%);
    min-height: 100vh;
}

[data-testid="stSidebar"] {
    background: var(--navy-mid) !important;
    border-right: 1px solid rgba(201,168,76,0.18) !important;
}
[data-testid="stSidebar"] * { color: var(--ivory) !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMarkdown p {
    color: var(--muted) !important;
    font-size: 0.82rem !important;
}

/* Hide Streamlit's default sidebar arrow toggle */
[data-testid="collapsedControl"] { display: none !important; }

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1280px !important;
}

.gold-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    border: none;
    margin: 1.6rem 0;
}

.ry-header-left { display: flex; align-items: center; gap: 1.2rem; }
.ry-logo {
    width: 54px; height: 54px;
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold-light) 100%);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.7rem;
    box-shadow: 0 4px 18px rgba(201,168,76,0.35);
    flex-shrink: 0;
}
.ry-title h1 {
    font-family: 'Playfair Display', serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--ivory);
    margin: 0; line-height: 1.1;
    letter-spacing: -0.3px;
}
.ry-title p {
    color: var(--gold);
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin: 4px 0 0;
}

.section-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 1rem;
}

.card {
    background: var(--navy-card);
    border: 1px solid rgba(201,168,76,0.15);
    border-radius: var(--radius);
    padding: 1.6rem 1.8rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1.2rem;
    transition: border-color 0.25s;
}
.card:hover { border-color: rgba(201,168,76,0.38); }

.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(201,168,76,0.2) !important;
    border-radius: 9px !important;
    color: var(--ivory) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s !important;
}
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.18) !important;
}
.stSelectbox label, .stNumberInput label {
    color: var(--muted) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px !important;
}
div[data-baseweb="select"] svg { color: var(--gold) !important; }

/* ── Gold CTA button ── */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    border: none !important;
    transition: all 0.22s ease !important;
    cursor: pointer !important;
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold-light) 100%) !important;
    color: var(--navy) !important;
    font-size: 0.88rem !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    padding: 0.85rem 2rem !important;
    box-shadow: 0 6px 24px rgba(201,168,76,0.38) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(201,168,76,0.52) !important;
    filter: brightness(1.06) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* ── Ghost style for the sidebar toggle button only ── */
div[data-testid="stButton"]:has(button[kind="secondary"]) > button,
button[kind="secondary"] {
    background: rgba(201,168,76,0.10) !important;
    color: var(--gold) !important;
    border: 1px solid rgba(201,168,76,0.40) !important;
    box-shadow: none !important;
    font-size: 0.75rem !important;
    letter-spacing: 1.5px !important;
    padding: 0.5rem 1rem !important;
}
button[kind="secondary"]:hover {
    background: rgba(201,168,76,0.22) !important;
    border-color: var(--gold) !important;
    transform: none !important;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(201,168,76,0.18);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: var(--ivory) !important; font-family: 'Playfair Display', serif !important; }
[data-testid="stMetricDelta"] { font-size: 0.78rem !important; }

.stProgress > div > div > div { background: var(--gold) !important; border-radius: 99px !important; }
.stProgress > div > div { background: rgba(255,255,255,0.08) !important; border-radius: 99px !important; }

.result-approved {
    background: linear-gradient(135deg, rgba(46,204,143,0.12), rgba(46,204,143,0.05));
    border: 1px solid rgba(46,204,143,0.45);
    border-left: 4px solid var(--success);
    border-radius: var(--radius);
    padding: 1.6rem 2rem;
    margin-top: 1rem;
}
.result-rejected {
    background: linear-gradient(135deg, rgba(224,92,107,0.12), rgba(224,92,107,0.05));
    border: 1px solid rgba(224,92,107,0.40);
    border-left: 4px solid var(--danger);
    border-radius: var(--radius);
    padding: 1.6rem 2rem;
    margin-top: 1rem;
}
.result-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
}
.result-sub { color: var(--muted); font-size: 0.85rem; line-height: 1.55; }

.feature-pill {
    display: inline-block;
    background: rgba(201,168,76,0.12);
    border: 1px solid rgba(201,168,76,0.25);
    border-radius: 99px;
    padding: 3px 12px;
    font-size: 0.72rem;
    color: var(--gold);
    margin: 3px 2px;
    font-weight: 500;
}
.step-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px; height: 26px;
    background: rgba(201,168,76,0.18);
    border: 1px solid rgba(201,168,76,0.35);
    border-radius: 50%;
    color: var(--gold);
    font-size: 0.7rem;
    font-weight: 700;
    margin-right: 8px;
}

/* Info panel expander styling */
[data-testid="stExpander"] {
    background: var(--navy-card) !important;
    border: 1px solid rgba(201,168,76,0.2) !important;
    border-radius: var(--radius) !important;
}
[data-testid="stExpander"] summary {
    color: var(--gold) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3.  MODEL LOADING
# ─────────────────────────────────────────────
MODEL_FILENAME = 'loan_model.pkl'
model_path = os.path.join('models', MODEL_FILENAME)

@st.cache_resource
def load_my_model():
    return joblib.load(model_path)

try:
    model = load_my_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    model_error = str(e)

# ─────────────────────────────────────────────
# 4.  SIDEBAR TOGGLE STATE
# ─────────────────────────────────────────────
if "panel_open" not in st.session_state:
    st.session_state.panel_open = False

# ─────────────────────────────────────────────
# 5.  SIDEBAR CONTENT
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem;">
        <div style="font-family:'Playfair Display',serif; font-size:1.15rem; color:#f4f0e8; font-weight:700;">
            R&amp;Y Credit
        </div>
        <div style="font-size:0.65rem; letter-spacing:2.5px; color:#c9a84c; text-transform:uppercase; margin-top:2px;">
            Intelligence Suite
        </div>
    </div>
    <hr style="border:none; border-top:1px solid rgba(201,168,76,0.2); margin:1rem 0;">
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">About the Model</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#8a9bae; font-size:0.82rem; line-height:1.6;">
    This tool uses a supervised machine learning model trained on historical loan application data
    to assess credit risk and support underwriting decisions.
    </p>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label" style="margin-top:1.2rem;">Model Features</div>', unsafe_allow_html=True)
    features = ["Gender", "Marital Status", "Dependents", "Education",
                "Employment", "Income", "Loan Amount", "Loan Term",
                "Credit History", "Property Area"]
    pills_html = "".join(f'<span class="feature-pill">{f}</span>' for f in features)
    st.markdown(pills_html, unsafe_allow_html=True)

    st.markdown('<hr style="border:none;border-top:1px solid rgba(201,168,76,0.2);margin:1.4rem 0;">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Model Status</div>', unsafe_allow_html=True)

    if model_loaded:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;font-size:0.82rem;color:#2ecc8f;">
            <div style="width:8px;height:8px;border-radius:50%;background:#2ecc8f;
                        box-shadow:0 0 8px rgba(46,204,143,0.7);"></div>
            Model loaded &amp; ready
        </div>""", unsafe_allow_html=True)
        try:
            st.markdown(f'<p style="color:#8a9bae;font-size:0.75rem;margin-top:6px;">Engine: {type(model).__name__}</p>',
                        unsafe_allow_html=True)
        except:
            pass
    else:
        st.markdown(f"""
        <div style="color:#e05c6b;font-size:0.82rem;">⚠ Model unavailable<br>
        <span style="font-size:0.72rem;color:#8a9bae;">{model_error}</span></div>
        """, unsafe_allow_html=True)

    st.markdown('<hr style="border:none;border-top:1px solid rgba(201,168,76,0.2);margin:1.4rem 0;">', unsafe_allow_html=True)
    st.markdown("""
    <p style="color:#8a9bae;font-size:0.7rem;text-align:center;line-height:1.6;">
    For internal use only.<br>
    Decisions are advisory and subject to compliance review.<br><br>
    © 2025 R&amp;Y Financial Group
    </p>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 6.  MAIN CONTENT
# ─────────────────────────────────────────────
if not model_loaded:
    st.error(f"Critical: Model could not be loaded — {model_error}")
    st.stop()

# ── Header: logo+title left | toggle button right ──
hdr_left, hdr_right = st.columns([5, 1])

with hdr_left:
    st.markdown("""
    <div class="ry-header-left">
        <div class="ry-logo">🏦</div>
        <div class="ry-title">
            <h1>R&amp;Y Credit Intelligence</h1>
            <p>Automated Underwriting &amp; Risk Assessment Platform</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with hdr_right:
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    btn_label = "✕  Close Info" if st.session_state.panel_open else "☰  About / Info"
    if st.button(btn_label, key="panel_toggle", type="secondary", use_container_width=True):
        st.session_state.panel_open = not st.session_state.panel_open
        st.rerun()

st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

# ── Inline info panel ──
if st.session_state.panel_open:
    with st.expander("ℹ️  R&Y Credit Intelligence — Model Information & Features", expanded=True):
        ic1, ic2, ic3 = st.columns(3)
        with ic1:
            st.markdown("""**About the Model**  
<span style='color:#8a9bae;font-size:0.82rem;line-height:1.6;'>
A supervised ML model trained on historical loan data to assess credit risk and
support underwriting decisions.
</span>""", unsafe_allow_html=True)
        with ic2:
            st.markdown("**Model Features**")
            features_panel = ["Gender", "Marital Status", "Dependents", "Education",
                              "Employment", "Income", "Loan Amount", "Loan Term",
                              "Credit History", "Property Area"]
            st.markdown("".join(f'<span class="feature-pill">{f}</span>' for f in features_panel),
                        unsafe_allow_html=True)
        with ic3:
            st.markdown("**Model Status**")
            if model_loaded:
                st.markdown("""
                <div style='display:flex;align-items:center;gap:8px;font-size:0.82rem;color:#2ecc8f;'>
                    <div style='width:8px;height:8px;border-radius:50%;background:#2ecc8f;
                                box-shadow:0 0 8px rgba(46,204,143,0.7);'></div>
                    Model loaded &amp; ready
                </div>""", unsafe_allow_html=True)
                try:
                    st.markdown(f'<p style="color:#8a9bae;font-size:0.75rem;margin-top:6px;">Engine: {type(model).__name__}</p>',
                                unsafe_allow_html=True)
                except:
                    pass
            else:
                st.markdown('<div style="color:#e05c6b;font-size:0.82rem;">⚠ Model unavailable</div>',
                            unsafe_allow_html=True)

col_desc, col_stats = st.columns([3, 1])
with col_desc:
    st.markdown("""
    <p style="color:#8a9bae; font-size:0.88rem; line-height:1.65; max-width:620px;">
    Complete the applicant profile below and run the credit analysis engine to receive an
    instant risk-based recommendation. All fields are required for an accurate assessment.
    </p>
    """, unsafe_allow_html=True)
with col_stats:
    st.markdown("""
    <div style="text-align:right;">
        <span style="font-size:0.68rem;letter-spacing:2px;text-transform:uppercase;color:#c9a84c;">
        AI-Powered · Real-Time
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 7.  INPUT CARDS
# ─────────────────────────────────────────────
left_col, right_col = st.columns(2, gap="large")

with left_col:
    with st.container():
        st.markdown("""
        <div class="card">
            <div class="section-label"><span class="step-badge">1</span>Applicant Profile</div>
        </div>
        """, unsafe_allow_html=True)
        gender     = st.selectbox("Gender", ["Male", "Female"])
        married    = st.selectbox("Marital Status", ["No", "Yes"],
                                  format_func=lambda x: "Married" if x == "Yes" else "Single / Unmarried")
        education  = st.selectbox("Education Level", ["Graduate", "Not Graduate"])
        dependents = st.selectbox("Number of Dependents", ["0", "1", "2", "3+"])
        self_emp   = st.selectbox("Employment Type", ["No", "Yes"],
                                  format_func=lambda x: "Self-Employed" if x == "Yes" else "Salaried / Employed")

with right_col:
    with st.container():
        st.markdown("""
        <div class="card">
            <div class="section-label"><span class="step-badge">2</span>Financial Details</div>
        </div>
        """, unsafe_allow_html=True)
        app_income    = st.number_input("Applicant Monthly Income ($)", min_value=0, value=5000, step=500)
        coapp_income  = st.number_input("Co-applicant Monthly Income ($)", min_value=0, value=0, step=500)
        loan_amt      = st.number_input("Loan Amount Requested ($000s)", min_value=0, value=150, step=10)
        term          = st.number_input("Loan Term (Days)", min_value=0, value=360, step=30)
        credit_hist   = st.selectbox("Credit History Status", ["Clear", "Not Clear"],
                                     format_func=lambda x: "✓ Clear — No prior defaults" if x == "Clear"
                                                           else "✗ Not Clear — Prior default(s) recorded")
        property_area = st.selectbox("Property Location", ["Rural", "Semiurban", "Urban"])

# ─────────────────────────────────────────────
# 8.  ANALYSIS BUTTON
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
run_btn = st.button("⚡  RUN CREDIT ANALYSIS", use_container_width=True)

# ─────────────────────────────────────────────
# 9.  PREDICTION & RESULTS
# ─────────────────────────────────────────────
if run_btn:
    data = {
        'Gender':            1 if gender == "Male" else 0,
        'Married':           1 if married == "Yes" else 0,
        'Dependents':        3 if dependents == "3+" else int(dependents),
        'Education':         0 if education == "Graduate" else 1,
        'Self_Employed':     1 if self_emp == "Yes" else 0,
        'ApplicantIncome':   app_income,
        'CoapplicantIncome': coapp_income,
        'LoanAmount':        loan_amt,
        'Loan_Amount_Term':  term,
        'Credit_History':    1.0 if credit_hist == "Clear" else 0.0,
        'Property_Area':     {"Rural": 0, "Semiurban": 1, "Urban": 2}[property_area],
    }
    input_df = pd.DataFrame([data])

    with st.spinner(""):
        ph = st.empty()
        bar = ph.progress(0)
        for label, pct in [
            ("Validating applicant profile…",  30),
            ("Running credit risk model…",      65),
            ("Compiling underwriting report…",  90),
            ("Finalising recommendation…",     100),
        ]:
            time.sleep(0.32)
            bar.progress(pct, text=label)
        time.sleep(0.25)
        ph.empty()

    prediction = model.predict(input_df)

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(input_df)[0]
        reject_pct  = round(proba[0] * 100, 1)
        approve_pct = round(proba[1] * 100, 1)
    else:
        approve_pct = 100 if prediction[0] == 1 else 0
        reject_pct  = 100 - approve_pct

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Analysis Results</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    total_income = app_income + coapp_income
    dti_ratio    = round((loan_amt * 1000) / (total_income * 12) * 100, 1) if total_income > 0 else 0

    with m1:
        st.metric("Approval Confidence", f"{approve_pct}%",
                  delta="Above threshold" if approve_pct >= 60 else "Below threshold",
                  delta_color="normal" if approve_pct >= 60 else "inverse")
    with m2:
        st.metric("Default Risk Score", f"{reject_pct}%",
                  delta="Low risk" if reject_pct < 40 else "High risk",
                  delta_color="inverse" if reject_pct >= 40 else "normal")
    with m3:
        st.metric("Total Household Income", f"${total_income:,}/mo")
    with m4:
        st.metric("Debt-to-Income Ratio", f"{dti_ratio}%",
                  delta="Acceptable" if dti_ratio <= 43 else "Elevated",
                  delta_color="normal" if dti_ratio <= 43 else "inverse")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p style="color:#8a9bae;font-size:0.77rem;letter-spacing:1px;text-transform:uppercase;">Approval Confidence</p>',
                unsafe_allow_html=True)
    st.progress(int(approve_pct))
    st.markdown("<br>", unsafe_allow_html=True)

    if prediction[0] == 1:
        st.markdown(f"""
        <div class="result-approved">
            <div class="result-title" style="color:#2ecc8f;">✅ &nbsp;Application Approved</div>
            <div class="result-sub">
                Based on the applicant's financial profile and credit history, the model recommends
                <strong style="color:#f4f0e8;">approval</strong> with a confidence score of
                <strong style="color:#2ecc8f;">{approve_pct}%</strong>. The assessed risk of default
                is <strong style="color:#f4f0e8;">{reject_pct}%</strong>, within acceptable thresholds.<br><br>
                <span style="font-size:0.78rem;opacity:0.75;">
                Advisory only. Final approval subject to compliance review and regulatory obligations.
                </span>
            </div>
        </div>""", unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown(f"""
        <div class="result-rejected">
            <div class="result-title" style="color:#e05c6b;">❌ &nbsp;Application Declined</div>
            <div class="result-sub">
                A <strong style="color:#e05c6b;">high probability of default ({reject_pct}%)</strong>
                was detected. The application does not meet current underwriting criteria.<br><br>
                <strong style="color:#f4f0e8;">Primary risk factors may include:</strong>
                poor credit history, high debt-to-income ratio, or insufficient income.<br><br>
                <span style="font-size:0.78rem;opacity:0.75;">
                Applicants may reapply after improving their financial standing.
                This outcome does not constitute a legal credit refusal notice.
                </span>
            </div>
        </div>""", unsafe_allow_html=True)