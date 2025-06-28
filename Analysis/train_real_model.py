import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

print("🏎️ F1 Position Predictor - Training with Real Data")
print("=" * 60)

# Load the data
csv_path = "driver_stats.csv"
print(f"🔍 Loading data from: {csv_path}")

try:
    df = pd.read_csv(csv_path)
    print(f"✅ Data loaded: {df.shape[0]} records, {df.shape[1]} columns")
    print(f"📋 Columns: {df.columns.tolist()}")
except Exception as e:
    print(f"❌ Error loading data: {e}")
    exit(1)

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace('.', '', regex=False)
print(f"📋 Cleaned columns: {df.columns.tolist()}")

# Check what position data looks like
print(f"\n📊 Position data sample:")
print(df[['driver', 'team', 'season', 'pos']].head(10))

# Convert position to numeric and clean
df['pos_numeric'] = pd.to_numeric(df['pos'], errors='coerce')

# Filter valid positions (1-20, exclude DNF, DSQ, etc.)
df_clean = df[df['pos_numeric'].notna() & (df['pos_numeric'] >= 1) & (df['pos_numeric'] <= 20)].copy()
print(f"📊 Clean data: {len(df_clean)} records with valid positions (1-20)")

if len(df_clean) < 50:
    print("❌ Not enough clean data for training. Creating synthetic data...")
    
    # Create synthetic training data
    np.random.seed(42)
    seasons = [2020, 2021, 2022, 2023, 2024]
    teams = list(range(10))  # 10 teams
    experiences = [1, 2, 3, 5, 8, 10, 15]
    
    synthetic_data = []
    for _ in range(1000):  # Create 1000 synthetic records
        season = np.random.choice(seasons)
        team = np.random.choice(teams)
        experience = np.random.choice(experiences)
        
        # Simulate realistic position based on team performance
        if team in [0, 1, 2]:  # Top teams (Red Bull, Mercedes, Ferrari)
            position = np.random.choice(range(1, 6), p=[0.4, 0.25, 0.15, 0.1, 0.1])
        elif team in [3, 4]:  # Mid teams (McLaren, Aston Martin)
            position = np.random.choice(range(1, 11), p=[0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.03, 0.01, 0.01])
        else:  # Lower teams
            position = np.random.choice(range(6, 21), p=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.08, 0.07, 0.05, 0.05, 0.03, 0.01, 0.01, 0.01])
        
        # Experience factor (better drivers get better positions)
        if experience >= 10:
            position = max(1, position - 2)  # Experienced drivers get better positions
        elif experience <= 2:
            position = min(20, position + 2)  # Rookies get worse positions
            
        synthetic_data.append({
            'season': season,
            'team_encoded': team,
            'driver_experience': experience,
            'position': position
        })
    
    df_model = pd.DataFrame(synthetic_data)
    print(f"✅ Created {len(df_model)} synthetic training records")
    
else:
    # Use real data
    print(f"✅ Using real data for training")
    
    # Create team mapping
    unique_teams = df_clean['team'].unique()
    team_mapping = {team: i for i, team in enumerate(unique_teams)}
    print(f"🏁 Team mapping: {team_mapping}")
    
    # Encode teams
    df_clean['team_encoded'] = df_clean['team'].map(team_mapping)
    
    # Create driver experience (simplified - count seasons per driver)
    driver_seasons = df_clean.groupby('driver')['season'].nunique().to_dict()
    df_clean['driver_experience'] = df_clean['driver'].map(driver_seasons)
    
    # Prepare model data
    df_model = df_clean[['season', 'team_encoded', 'driver_experience', 'pos_numeric']].copy()
    df_model.rename(columns={'pos_numeric': 'position'}, inplace=True)
    df_model = df_model.dropna()

print(f"\n📊 Model training data:")
print(f"   Records: {len(df_model)}")
print(f"   Features: season, team_encoded, driver_experience")
print(f"   Target: position (1-20)")
print(f"   Position range: {df_model['position'].min()} to {df_model['position'].max()}")

# Check position distribution
print(f"\n🏁 Position distribution (top 10):")
pos_counts = df_model['position'].value_counts().sort_index()
for pos in range(1, min(11, int(df_model['position'].max()) + 1)):
    count = pos_counts.get(pos, 0)
    print(f"   P{pos}: {count} records")

# Prepare features and target
features = ['season', 'team_encoded', 'driver_experience']
X = df_model[features].copy()
y = df_model['position'].copy().astype(int)

print(f"\n🎯 Final training data:")
print(f"   X shape: {X.shape}")
print(f"   y shape: {y.shape}")
print(f"   Unique positions: {sorted(y.unique())}")

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"\n🔀 Data split:")
print(f"   Training: {X_train.shape[0]} samples")
print(f"   Testing: {X_test.shape[0]} samples")

# Train the model
print(f"\n🤖 Training Random Forest Classifier...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)
print(f"✅ Model training complete!")

# Evaluate
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

train_accuracy = accuracy_score(y_train, y_pred_train)
test_accuracy = accuracy_score(y_test, y_pred_test)

print(f"\n📊 Model Performance:")
print(f"   Training Accuracy: {train_accuracy:.3f}")
print(f"   Test Accuracy: {test_accuracy:.3f}")

# Feature importance
print(f"\n🎯 Feature Importance:")
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for _, row in feature_importance.iterrows():
    print(f"   {row['feature']}: {row['importance']:.3f}")

# Test some predictions
print(f"\n🧪 Test Predictions:")
test_cases = [
    [2024, 0, 10],  # Red Bull, experienced
    [2024, 1, 8],   # Mercedes, experienced  
    [2024, 8, 2],   # Williams, rookie
]

for case in test_cases:
    pred = model.predict([case])[0]
    prob = model.predict_proba([case])[0]
    conf = max(prob)
    
    print(f"   Input: season={case[0]}, team={case[1]}, exp={case[2]} → P{pred} (conf: {conf:.3f})")

# Save the model
model_path = "f1_position_predictor.joblib"
joblib.dump(model, model_path)
print(f"\n💾 Model saved as '{model_path}'")

# Save model info
model_info = {
    'features': features,
    'team_mapping': {
        "Red Bull Racing": 0, "Mercedes": 1, "Ferrari": 2, "McLaren": 3,
        "Aston Martin": 4, "Alpine": 5, "Haas": 6, "RB": 7,
        "Williams": 8, "Kick Sauber": 9
    },
    'model_type': 'position_classification',
    'classes': model.classes_.tolist(),
    'accuracy': test_accuracy
}
joblib.dump(model_info, "f1_model_info.joblib")
print(f"💾 Model info saved as 'f1_model_info.joblib'")

print(f"\n✅ Position prediction model ready!")
print(f"🎯 Model can predict positions 1-{y.max()} with {test_accuracy:.1%} accuracy")
