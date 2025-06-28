#!/usr/bin/env python3

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

print("🏎️ Simple F1 Position Predictor - Training Model")
print("="*50)

# Get CSV path
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "..", "Scraper", "driver_stats.csv")

print(f"🔍 Looking for CSV at: {csv_path}")
if not os.path.exists(csv_path):
    print("❌ CSV not found, creating minimal synthetic data")
    # Create minimal synthetic data
    synthetic_data = {
        'season': [2020, 2020, 2021, 2021, 2022, 2022, 2023, 2023] * 3,
        'driver': ['Hamilton', 'Verstappen', 'Hamilton', 'Verstappen', 'Leclerc', 'Verstappen', 'Verstappen', 'Norris'] * 3,
        'team': ['Mercedes', 'Red Bull Racing', 'Mercedes', 'Red Bull Racing', 'Ferrari', 'Red Bull Racing', 'Red Bull Racing', 'McLaren'] * 3,
        'pos': [1, 2, 3, 1, 2, 1, 1, 4] * 3,
        'pts': [25, 18, 15, 25, 18, 25, 25, 12] * 3
    }
    df = pd.DataFrame(synthetic_data)
    print(f"📊 Created synthetic data: {len(df)} records")
else:
    print("✅ Loading CSV data")
    df = pd.read_csv(csv_path)
    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace('.', '', regex=False)
    print(f"📊 Data loaded: {len(df)} records")

# Team mapping for encoding
team_mapping = {
    "Red Bull Racing": 0, "Mercedes": 1, "Ferrari": 2, "McLaren": 3,
    "Aston Martin": 4, "Alpine": 5, "Haas": 6, "RB": 7,
    "Williams": 8, "Kick Sauber": 9, "AlphaTauri": 7, "Alfa Romeo": 9
}

print(f"🏁 Team mapping: {team_mapping}")

# Prepare data for modeling
print("🧹 Preparing data...")

# Clean position data (handle numeric positions only)
df['pos_numeric'] = pd.to_numeric(df['pos'], errors='coerce')
df = df.dropna(subset=['pos_numeric'])
df = df[df['pos_numeric'] > 0]  # Only valid finishing positions
df = df[df['pos_numeric'] <= 20]  # Reasonable position limit

print(f"📈 Valid position records: {len(df)}")
print(f"📊 Position range: {df['pos_numeric'].min()} to {df['pos_numeric'].max()}")

# Encode teams
def encode_team(team_name):
    team_name = str(team_name).strip()
    # Direct mapping
    if team_name in team_mapping:
        return team_mapping[team_name]
    
    # Fuzzy matching for team name variations
    for team, code in team_mapping.items():
        if team.lower() in team_name.lower() or team_name.lower() in team.lower():
            return code
    
    # Default for unknown teams
    return 9  # Default to Kick Sauber encoding

df['team_encoded'] = df['team'].apply(encode_team)
print(f"🏢 Team encoding completed")

# Create driver experience feature (simplified)
driver_seasons = df.groupby('driver')['season'].nunique()
df['driver_experience'] = df['driver'].map(driver_seasons).fillna(1)

print(f"👨‍💼 Driver experience calculated")

# Prepare features and target
# Features: [season, team_encoded, driver_experience]
X = df[['season', 'team_encoded', 'driver_experience']].values
y = df['pos_numeric'].values.astype(int)

print(f"🎯 Features shape: {X.shape}")
print(f"🎯 Target shape: {y.shape}")
print(f"🎯 Unique positions to predict: {sorted(np.unique(y))}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"🔄 Train/test split: {X_train.shape[0]} train, {X_test.shape[0]} test")

# Train model
print("🤖 Training RandomForest model...")
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    max_depth=10
)

model.fit(X_train, y_train)

# Test model
y_pred = model.predict(X_test)
accuracy = (y_pred == y_test).mean()

print(f"✅ Model trained successfully!")
print(f"🎯 Test accuracy: {accuracy:.3f}")
print(f"📊 Model classes: {model.classes_}")

# Save model
model_path = "f1_position_predictor.joblib"
joblib.dump(model, model_path)
print(f"💾 Model saved to: {model_path}")

# Save model info
model_info = {
    'features': ['season', 'team_encoded', 'driver_experience'],
    'team_mapping': team_mapping,
    'model_type': 'position_classification',
    'classes': model.classes_.tolist(),
    'accuracy': accuracy
}

info_path = "f1_model_info.joblib"
joblib.dump(model_info, info_path)
print(f"💾 Model info saved to: {info_path}")

# Test predictions
print("\n🧪 Testing predictions...")
test_cases = [
    [2024, 0, 3],  # Red Bull, experienced driver
    [2024, 1, 1],  # Mercedes, rookie
    [2024, 2, 5],  # Ferrari, very experienced
    [2023, 3, 2],  # McLaren, 2 years experience
]

for i, test_case in enumerate(test_cases):
    pred = model.predict([test_case])
    proba = model.predict_proba([test_case])
    team_name = next((team for team, code in team_mapping.items() if code == test_case[1]), f"Team {test_case[1]}")
    
    print(f"Test {i+1}: Season {test_case[0]}, {team_name}, {test_case[2]} years exp")
    print(f"  -> Position: P{pred[0]}, Confidence: {np.max(proba[0]):.3f}")

print("\n✅ Model training completed successfully!")
