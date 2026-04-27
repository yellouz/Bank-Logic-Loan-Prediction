import pandas as pd
import joblib
import os

print("[System] Booting up AI Brain...")

# 1. Locate and load the frozen brain
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, '..', 'models', 'loan_model.pkl')

# Load the AI
try:
    model = joblib.load(model_path)
    print("[System] Brain loaded successfully.")
except FileNotFoundError:
    print("[Error] Could not find the AI model. Did you run train.py first?")
    exit()

# 2. Create a new customer profile
# We have to give the AI the exact same 11 details it studied in class.
print("\n[System] Entering new customer data...")
new_customer = pd.DataFrame([{
    'Gender': 1,               # 1 for Male
    'Married': 1,              # 1 for Yes
    'Dependents': 0,           # 0 dependents
    'Education': 0,            # 0 for Graduate (based on our encoder)
    'Self_Employed': 0,        # 0 for No
    'ApplicantIncome': 6000,   # Monthly income
    'CoapplicantIncome': 2000, # Partner's income
    'LoanAmount': 150.0,       # Loan amount in thousands
    'Loan_Amount_Term': 360.0, # 360 months (30 years)
    'Credit_History': 1.0,     # 1.0 is Good Credit! (The most important factor)
    'Property_Area': 2         # 2 for Urban
}])

# 3. Ask the AI for a decision
print("[System] Analyzing Customer Profile...")
prediction = model.predict(new_customer)

# 4. Display the Result
print("\n=========================================")
if prediction[0] == 1:
    print("🎉 RESULT: LOAN APPROVED!")
else:
    print("❌ RESULT: LOAN DENIED.")
print("=========================================")