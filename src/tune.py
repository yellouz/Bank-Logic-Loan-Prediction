import pandas as pd
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# --- 1. LOAD AND SPLIT DATA ---
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, '..', 'data', 'processed.csv')
data = pd.read_csv(input_path)

X = data.drop(columns=['Loan_ID', 'Loan_Status']) 
Y = data['Loan_Status']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# --- 2. THE ENGINEER'S FIX: SCALING ---
# Now Python knows exactly what X_train_scaled is!
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# --- 3. GRID SEARCH TUNING ---
# Tell the grid which combinations to test
param_grid = {
    'n_estimators': [100, 200, 300, 500],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'class_weight': ['balanced', None] # Crucial for banking!
}

print("[System] Running Grid Search. This might take a minute or two...")

# cv=5 means it double-checks its math 5 times for every combination
grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train_scaled, Y_train)

print(f"\n🏆 Best Grid Accuracy Found: {grid_search.best_score_ * 100:.2f}%")
print(f"🔧 Best Settings: {grid_search.best_params_}")