import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

# --- 1. LOAD AND SPLIT DATA ---
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, '..', 'data', 'processed.csv')
data = pd.read_csv(input_path)

X = data.drop(columns=['Loan_ID', 'Loan_Status']) 
Y = data['Loan_Status']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# --- 1.5 SCALING THE DATA ---
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- 2. THE ALGORITHM DEATHMATCH ---
print("\n[System] Initiating Advanced Benchmarking (Accuracy, Precision, Recall)...")

models = {
    "Logistic Reg": LogisticRegression(random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "SVM": SVC(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42, min_samples_split=2, class_weight=None) # Using the best settings from our Grid Search
}

names = []
accuracies = []
precisions = []
recalls = []

for name, model in models.items():
    model.fit(X_train_scaled, Y_train)
    predictions = model.predict(X_test_scaled)
    
    # Calculate all three metrics (pos_label=1 assumes 1 means 'Approved')
    acc = accuracy_score(Y_test, predictions) * 100
    prec = precision_score(Y_test, predictions, pos_label=1) * 100
    rec = recall_score(Y_test, predictions, pos_label=1) * 100
    
    names.append(name)
    accuracies.append(acc)
    precisions.append(prec)
    recalls.append(rec)
    
    print(f"🥊 {name.ljust(15)} -> Accuracy: {acc:.1f}% | Precision: {prec:.1f}% | Recall: {rec:.1f}%")

print("\n[System] Benchmarking Complete. Generating Grouped Graph...")

# --- 3. DRAWING THE GROUPED GRAPH ---
plt.figure(figsize=(12, 7))

# Set the width of the bars and their positions
x = np.arange(len(names))  
width = 0.25  

# Plotting the three metrics side-by-side
# We use soft grays for Acc/Rec and our signature teal for Precision (the most important banking metric!)
rects1 = plt.bar(x - width, accuracies, width, label='Accuracy', color="#16488a")
rects2 = plt.bar(x, precisions, width, label='Precision (Bank Safety)', color="#991616")
rects3 = plt.bar(x + width, recalls, width, label='Recall (Customer Approval)', color="#0d7552")

plt.title('Algorithm Performance: Accuracy vs. Precision vs. Recall', fontsize=18, fontweight='bold', pad=20)
plt.ylabel('Score (%)', fontsize=12)
plt.xticks(x, names, fontsize=12, fontweight='bold')
plt.ylim(0, 115) # Extended Y-axis to make room for the text labels

# Clean up borders
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Add a legend to explain the colors
plt.legend(loc='lower right', fontsize=11)

# Function to auto-label the exact numbers on top of the bars
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2, height + 1, 
                 f"{height:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold', rotation=0)

add_labels(rects1)
add_labels(rects2)
add_labels(rects3)

# --- 4. SAVE THE IMAGE ---
output_image = os.path.join(script_dir, '..', 'advanced_algorithm_comparison.png')
plt.savefig(output_image, bbox_inches='tight', dpi=300) 

print(f"[Success] Advanced graph saved to: {output_image}")