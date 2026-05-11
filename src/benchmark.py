import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Import the competitors
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

# --- 1. LOAD AND SPLIT DATA (Your existing code) ---
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, '..', 'data', 'processed.csv')
data = pd.read_csv(input_path)

X = data.drop(columns=['Loan_ID', 'Loan_Status']) 
Y = data['Loan_Status']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# --- 2. THE ALGORITHM DEATHMATCH ---
print("\n[System] Initiating Algorithm Benchmarking...")

# Put all the algorithms into a dictionary
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Support Vector Machine": SVC(random_state=42),
    "Random Forest (Ours)": RandomForestClassifier(n_estimators=250, max_depth=10, random_state=42)
}

# Loop through them, train them, and print their scores
for name, model in models.items():
    # 1. Teach the machine
    model.fit(X_train, Y_train)
    
    # 2. Take the exam
    predictions = model.predict(X_test)
    
    # 3. Grade it
    score = accuracy_score(Y_test, predictions)
    
    print(f"🥊 {name}: {score * 100:.2f}%")

print("\n[System] Benchmarking Complete.")