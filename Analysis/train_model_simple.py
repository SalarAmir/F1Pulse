import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

print("🏎️ F1 Position Predictor - Simple Training")
print("="*50)

# Load the data
csv_path = "driver_stats.csv"
print(f"🔍 Loading data from: {csv_path}")

try:
    df = pd.read_csv(csv_path)
    print(f"✅ Data loaded: {df.shape[0]} records, {df.shape[1]} columns")
except Exception as e:
    print(f"❌ Error loading data: {e}")
    exit(1)

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace('.', '', regex=False)
print(f"📋 Columns: {df.columns.tolist()}")

# Clean and prepare data
print("\n🧹 Cleaning data...")

# Convert position to numeric (handle DNF, DSQ, etc.)
df['pos_numeric'] = pd.to_numeric(df['pos'], errors='coerce')

# Filter out non-finishing positions (DNF, DSQ, etc.)
df_clean = df[df['pos_numeric'].notna() & (df['pos_numeric'] > 0) & (df['pos_numeric'] <= 20)].copy()
print(f"📊 Clean data: {len(df_clean)} records with valid positions")

# Create team mapping
team_mapping = {}
unique_teams = df_clean['team'].unique()
for i, team in enumerate(unique_teams):
    team_mapping[team] = i

# Encode teams
df_clean['team_encoded'] = df_clean['team'].map(team_mapping)

# Create driver experience feature (simple version - just use a default)
df_clean['driver_experience'] = 3  # Default experience

# Prepare features
features = ['season', 'team_encoded', 'driver_experience']
X = df_clean[features].copy()
y = df_clean['pos_numeric'].copy().astype(int)

print(f"🎯 Features: {features}")
print(f"📊 Training data shape: {X.shape}")
print(f"🏁 Position range: {y.min()} to {y.max()}")

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
print("\n🤖 Training Random Forest Classifier...")
model = RandomForestClassifier(
    n_estimators=50,
    max_depth=8,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"📊 Test Accuracy: {accuracy:.3f}")

# Save the model
model_path = "f1_position_predictor.joblib"
joblib.dump(model, model_path)
print(f"💾 Model saved as '{model_path}'")

# Save model info
model_info = {
    'features': features,
    'team_mapping': team_mapping,
    'model_type': 'position_classification'
}
joblib.dump(model_info, "f1_model_info.joblib")
print(f"💾 Model info saved as 'f1_model_info.joblib'")

# Test prediction
test_input = [[2024, 0, 5]]
predicted_pos = model.predict(test_input)[0]
prob = model.predict_proba(test_input)[0]
confidence = max(prob)

print(f"\n🧪 Test prediction:")
print(f"  Input: season=2024, team=0, experience=5")
print(f"  Predicted position: P{predicted_pos} (confidence: {confidence:.3f})")

print(f"\n✅ Position prediction model ready!")
