import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

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

# --- 4. THE BRAIN: Training the Algorithm ---
print("\n[System] Injecting Algorithm: Random Forest...")

# We are changing 'n_estimators' (the number of decision-makers) from 100 to 250
# We are also adding 'max_depth' so they don't overthink and memorize the data
model = RandomForestClassifier(n_estimators=250, max_depth=10, random_state=42)

# Teaching the machine (This is the actual "Learning" command)
model.fit(X_train, Y_train)
print("[System] Training Complete.")

# --- 5. THE FINAL EXAM: Testing the Algorithm ---
print("\n[System] Administering Final Exam to the AI...")

# We give the AI the Test details (X_test), but we hide the answers (Y_test)
predictions = model.predict(X_test)

# --- 6. GRADING THE EXAM ---
# Now we compare the AI's guesses against the real, hidden answers
score = accuracy_score(Y_test, predictions)

print("=========================================")
print(f"🏆 AI Accuracy Score: {score * 100:.2f}%")
print("=========================================")

# --- 7. PEEKING INTO THE AI'S BRAIN ---
print("\n[System] Analyzing AI Decision Making...")

# We ask the model to rank how important each column was
importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\n🏆 Top 3 Most Important Factors for getting a Loan:")
print(importance.head(3))

# --- 8. FREEZING THE BRAIN ---
print("\n[System] Saving the trained model...")

# We save the 'model' variable into a physical file in your models folder
model_path = os.path.join(script_dir, '..', 'models', 'loan_model.pkl')
joblib.dump(model, model_path)

print(f"[Success] AI Brain saved to: {model_path}")