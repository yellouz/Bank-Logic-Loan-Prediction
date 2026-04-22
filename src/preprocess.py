import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder

print("[System] Firing up the Preprocessing Engine...")

# --- 1. SETUP PATHS (The Bulletproof Way) ---
# Find exactly where this script lives, then build the paths to the data folder
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, '..', 'data', 'train.csv')
output_path = os.path.join(script_dir, '..', 'data', 'processed.csv')

# --- 2. LOAD THE DATA ---
data = pd.read_csv(input_path)
print(f"Data loaded successfully. Total Customers: {data.shape[0]}")

# --- 3. IMPUTATION: Patching the holes ---
print("\n[System] Patching missing data...")

# Fill numerical holes with the Median
data['LoanAmount'] = data['LoanAmount'].fillna(data['LoanAmount'].median())
data['Loan_Amount_Term'] = data['Loan_Amount_Term'].fillna(data['Loan_Amount_Term'].median())

# Fill categorical (text) holes with the Mode (most frequent)
data['Credit_History'] = data['Credit_History'].fillna(data['Credit_History'].mode()[0])

text_columns = ['Gender', 'Married', 'Dependents', 'Self_Employed']
for col in text_columns:
    if col in data.columns:
        data[col] = data[col].fillna(data[col].mode()[0])

# --- 4. ENCODING: Translating text to numbers ---
print("\n[System] Translating text to numeric flags...")
encoder = LabelEncoder()
columns_to_encode = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area', 'Loan_Status']

for col in columns_to_encode:
    if col in data.columns:
        data[col] = encoder.fit_transform(data[col])

# --- 5. VERIFICATION & SAVING ---
print("\n--- Verification: Missing Data Count ---")
print(data.isnull().sum()) # Should all be zeros!

# Save the clean data to the new processed file
data.to_csv(output_path, index=False)
print(f"\n[Success] Clean data pipeline complete. Saved to: {output_path}")