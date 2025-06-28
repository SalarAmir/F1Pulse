import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

print("🏎️ F1 Position Predictor - Training Model")
print("="*50)

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "driver_stats.csv")

# Check if file exists, if not try the Scraper folder
if not os.path.exists(csv_path):
    csv_path = os.path.join(os.path.dirname(script_dir), "Scraper", "driver_stats.csv")

print(f"🔍 Looking for CSV file at: {csv_path}")
if os.path.exists(csv_path):
    print("✅ CSV file found!")
else:
    print("❌ CSV file not found!")
    exit(1)

# Load the data
df = pd.read_csv(csv_path)

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace('.', '', regex=False)

print(f"📊 Data loaded: {df.shape[0]} records, {df.shape[1]} columns")
print(f"📋 Columns: {df.columns.tolist()}")

# Basic data exploration
print(f"\n📈 Available seasons: {sorted(df['season'].unique())}")
print(f"🏁 Position range: {df['pos'].min()} to {df['pos'].max()}")

# Clean and prepare data
print("\n🧹 Cleaning data...")

# Clean driver names (remove driver codes like "HAM", "VER")
df['driver_clean'] = df['driver'].str.extract(r'^(.*?)\s?[A-Z]{2,3}$')[0]
df['driver_clean'] = df['driver_clean'].fillna(df['driver'])

# Convert position to numeric (handle DNF, DSQ, etc.)
df['pos_numeric'] = pd.to_numeric(df['pos'], errors='coerce')

# Remove rows where position couldn't be converted (DNF, DSQ, etc.)
df_clean = df.dropna(subset=['pos_numeric']).copy()
print(f"🔧 After cleaning: {len(df_clean)} records (removed {len(df) - len(df_clean)} non-finishing results)")

# Convert position to integer
df_clean['position'] = df_clean['pos_numeric'].astype(int)

# Create team encoding manually (more reliable than automatic encoding)
team_mapping = {
    "Red Bull Racing": 0, "Mercedes": 1, "Ferrari": 2, "McLaren": 3,
    "Aston Martin": 4, "Alpine": 5, "Haas": 6, "AlphaTauri": 7,
    "Williams": 8, "Alfa Romeo": 9, "RB": 7, "Kick Sauber": 9
}

def encode_team(team_name):
    """Encode team name to number"""
    team_lower = str(team_name).lower()
    for team, code in team_mapping.items():
        if team.lower() in team_lower or any(word in team_lower for word in team.lower().split()):
            return code
    
    # Handle special cases
    if 'red bull' in team_lower:
        return 0  # Red Bull Racing
    elif 'mercedes' in team_lower:
        return 1
    elif 'ferrari' in team_lower:
        return 2
    elif 'mclaren' in team_lower:
        return 3
    elif 'aston' in team_lower:
        return 4
    elif 'alpine' in team_lower or 'renault' in team_lower:
        return 5
    elif 'haas' in team_lower:
        return 6
    elif 'alphatauri' in team_lower or 'rb ' in team_lower:
        return 7
    elif 'williams' in team_lower:
        return 8
    elif 'alfa' in team_lower or 'sauber' in team_lower:
        return 9
    else:
        return 10  # Unknown team

df_clean['team_encoded'] = df_clean['team'].apply(encode_team)

print(f"\n🏎️ Team encoding distribution:")
team_counts = df_clean['team_encoded'].value_counts().sort_index()
for code, count in team_counts.items():
    team_name = [k for k, v in team_mapping.items() if v == code]
    team_name = team_name[0] if team_name else f"Team {code}"
    print(f"  {code}: {team_name} - {count} records")

# Feature engineering
print("\n⚙️ Engineering features...")

# Add driver experience (how many seasons they've raced)
df_clean['driver_experience'] = df_clean.groupby('driver_clean')['season'].transform('nunique')

# Add season-based features
df_clean['season_normalized'] = (df_clean['season'] - df_clean['season'].min()) / (df_clean['season'].max() - df_clean['season'].min())

# Prepare features and target
print("\n🎯 Preparing features and target...")

# Features: season, team_encoded, driver_experience
features = ['season', 'team_encoded', 'driver_experience']
X = df_clean[features].copy()
y = df_clean['position'].copy()

print(f"📊 Features: {features}")
print(f"🎯 Target: position (1-{y.max()})")
print(f"🧮 Training data shape: {X.shape}")

# Display feature statistics
print(f"\n📈 Feature statistics:")
print(X.describe())

print(f"\n🏁 Position distribution:")
position_counts = y.value_counts().sort_index()
for pos in range(1, min(11, y.max() + 1)):  # Show top 10 positions
    count = position_counts.get(pos, 0)
    print(f"  P{pos}: {count} occurrences")

# Split the data
print("\n🔀 Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=None)

print(f"Training set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# Train the model (using classifier instead of regressor)
print("\n🤖 Training Random Forest Classifier...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Make predictions
print("\n🔮 Making predictions...")
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Evaluate the model
print("\n📊 Model Performance:")
train_accuracy = accuracy_score(y_train, y_pred_train)
test_accuracy = accuracy_score(y_test, y_pred_test)

print(f"Training Accuracy: {train_accuracy:.3f}")
print(f"Test Accuracy: {test_accuracy:.3f}")

# Feature importance
print(f"\n🎯 Feature Importance:")
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for _, row in feature_importance.iterrows():
    print(f"  {row['feature']}: {row['importance']:.3f}")

# Classification report for top positions
print(f"\n📈 Detailed Performance (Top 10 positions):")
positions_to_show = list(range(1, min(11, y.max() + 1)))
report = classification_report(
    y_test, 
    y_pred_test, 
    labels=positions_to_show,
    target_names=[f"P{i}" for i in positions_to_show],
    zero_division=0
)
print(report)

# Save the model
model_path = "f1_position_predictor.joblib"
joblib.dump(model, model_path)
print(f"\n💾 Model saved as '{model_path}'")

# Save feature information
feature_info = {
    'features': features,
    'team_mapping': team_mapping,
    'model_type': 'position_classification'
}
joblib.dump(feature_info, "f1_model_info.joblib")
print(f"💾 Model info saved as 'f1_model_info.joblib'")

# Test predictions with some examples
print(f"\n🧪 Sample Predictions:")
test_cases = [
    {'season': 2024, 'team_encoded': 0, 'driver_experience': 5, 'description': '2024 Red Bull experienced driver'},
    {'season': 2024, 'team_encoded': 1, 'driver_experience': 10, 'description': '2024 Mercedes veteran'},
    {'season': 2024, 'team_encoded': 8, 'driver_experience': 2, 'description': '2024 Williams rookie'},
]

for case in test_cases:
    pred_input = [[case['season'], case['team_encoded'], case['driver_experience']]]
    predicted_position = model.predict(pred_input)[0]
    probability = model.predict_proba(pred_input)[0]
    confidence = max(probability)
    
    print(f"  {case['description']}")
    print(f"    → Predicted position: P{predicted_position} (confidence: {confidence:.2f})")

print(f"\n✅ Position prediction model training complete!")
print(f"🎯 Model predicts finishing positions (1-{y.max()}) based on:")
print(f"   - Season")
print(f"   - Team (encoded)")  
print(f"   - Driver experience")
