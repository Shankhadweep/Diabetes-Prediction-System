import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load the diabetes dataset
df = pd.read_csv('abm2.csv')  # Make sure you have this file

# Separate features and target
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model properly
with open('diabetes_model.sav', 'wb') as file:
    pickle.dump(model, file)

# Optional: Print accuracy score
print(f"Model accuracy: {model.score(X_test, y_test):.2f}")