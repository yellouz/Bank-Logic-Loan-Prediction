import pandas as pd
import os
from sklearn.model_selection import train_test_split


print("[System] Initializing Training Sequence...")

# 1. Load the clean data
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, '..', 'data', 'processed.csv')
data = pd.read_csv(input_path)

# 2. Split the data into Features (X) and Target (Y)
# We drop 'Loan_ID' because a random string of letters doesn't help predict a loan.
# We drop 'Loan_Status' from X because that is the answer key!
X = data.drop(columns=['Loan_ID', 'Loan_Status']) 
Y = data['Loan_Status'] # This is the answer key

print(f"Features (X) shape: {X.shape}")
print(f"Target (Y) shape: {Y.shape}")
print("\n[System] Data split successful. Ready for algorithm injection.")

# ... (your previous code that defined X and Y is up here) ...

# --- 3. CREATE THE STUDY GUIDE AND THE FINAL EXAM ---
print("\n[System] Splitting data into Training and Testing sets...")

# This automatically shuffles the data and splits it 80/20
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

print(f"Study Material (X_train): {X_train.shape[0]} customers")
print(f"Final Exam (X_test): {X_test.shape[0]} customers")
print("\n[System] Ready for the algorithm. Awaiting Dev B.")