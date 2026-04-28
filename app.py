import streamlit as st
import joblib
import pandas as pd
import os

# --- 1. SETUP & MODEL LOADING ---
# Ensure this matches the EXACT name of your file in the 'models' folder
MODEL_FILENAME = 'loan_model.pkl' 
model_path = os.path.join('models', MODEL_FILENAME)

@st.cache_resource # This makes the app faster
def load_my_model():
    return joblib.load(model_path)

try:
    model = load_my_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# --- 2. THE INTERFACE ---
st.set_page_config(page_title="Bank Loan Prediction", page_icon="🏦")

st.title("🏦 Smart Loan Approval System")
st.markdown("### Decision Support Tool for Credit Risk Assessment")
st.write("---")

# Organized layout for your presentation
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Applicant Profile")
    gender = st.selectbox("Gender", ["Male", "Female"])
    married = st.selectbox("Married", ["No", "Yes"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    dependents = st.selectbox("Number of Dependents", ["0", "1", "2", "3+"])
    self_emp = st.selectbox("Self Employed", ["No", "Yes"])

with col2:
    st.subheader("💰 Financial Details")
    app_income = st.number_input("Applicant Income", min_value=0, value=5000)
    coapp_income = st.number_input("Co-applicant Income", min_value=0, value=0)
    loan_amt = st.number_input("Loan Amount (in thousands)", min_value=0, value=150)
    term = st.number_input("Term (Days)", min_value=0, value=360)
    credit_hist = st.selectbox("Credit History", ["Clear", "Not Clear"])
    property_area = st.selectbox("Property Area", ["Rural", "Semiurban", "Urban"])

# --- 3. THE MAGIC (PREDICTION) ---
if st.button("RUN CREDIT ANALYSIS", use_container_width=True):
    # Mapping the words back to the numbers your model needs
    data = {
        'Gender': 1 if gender == "Male" else 0,
        'Married': 1 if married == "Yes" else 0,
        'Dependents': 3 if dependents == "3+" else int(dependents),
        'Education': 0 if education == "Graduate" else 1,
        'Self_Employed': 1 if self_emp == "Yes" else 0,
        'ApplicantIncome': app_income,
        'CoapplicantIncome': coapp_income,
        'LoanAmount': loan_amt,
        'Loan_Amount_Term': term,
        'Credit_History': 1.0 if credit_hist == "Clear" else 0.0,
        'Property_Area': {"Rural": 0, "Semiurban": 1, "Urban": 2}[property_area]
    }
    
    input_df = pd.DataFrame([data])
    prediction = model.predict(input_df)
    
    st.write("---")
    if prediction[0] == 1:
        st.success("## ✅ LOAN APPROVED")
        st.balloons() # This adds a great "Wow" factor to the presentation
    else:
        st.error("## ❌ LOAN REJECTED")
        st.warning("High Probability of Default detected based on profile features.")