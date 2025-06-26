import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import joblib
import os

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "driver_stats.csv")

# Check if file exists, if not try the Scraper folder
if not os.path.exists(csv_path):
    csv_path = os.path.join(os.path.dirname(script_dir), "Scraper", "driver_stats.csv")

print(f"Looking for CSV file at: {csv_path}")
if os.path.exists(csv_path):
    print("✅ CSV file found!")
else:
    print("❌ CSV file not found!")
    exit(1)


# Load the CSV text (replace with actual file read in your case)
df = pd.read_csv(csv_path)  # Use the dynamically found CSV path

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace('.', '', regex=False)

# Print column names to debug
print("Available columns:", df.columns.tolist())
print("Data shape:", df.shape)
print("First few rows:")
print(df.head())

# Clean data
df['driver_clean'] = df['driver'].str.extract(r'^(.*?)\s?[A-Z]{2,3}$')  # Extract name
df['pts'] = pd.to_numeric(df['pts'], errors='coerce')  # Ensure points are numeric
df['season'] = pd.to_numeric(df['season'], errors='coerce')
df['driver_experience'] = df.groupby('driver_clean')['season'].transform(lambda x: x.rank(method='dense'))

# Add team encoding
# df = pd.get_dummies(df, columns=['car'], prefix='team', drop_first=True)

# Let's check what team/car column is actually called
team_columns = [col for col in df.columns if 'team' in col.lower() or 'car' in col.lower()]
print("Team/Car related columns:", team_columns)

# Encode team names - find the correct team column
team_column = None
for col in df.columns:
    if 'team' in col.lower():
        team_column = col
        break

if team_column:
    le_team = LabelEncoder()
    df['team_encoded'] = le_team.fit_transform(df[team_column].astype(str))
    print(f"Using column '{team_column}' for team encoding")
else:
    print("No team column found, creating dummy encoding")
    df['team_encoded'] = 0  # fallback

# Drop missing values (NaNs)
df.dropna(subset=['pts', 'season', 'team_encoded'], inplace=True)

# Prepare training data
X = df[['season', 'team_encoded']]
y = df['pts']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f"R² Score: {r2:.4f}")
print(f"R² Score: {r2:.4f}")
print(f"Mean Squared Error: {mse:.2f}")
print("R² Score:", r2_score(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))

# Save the trained model
joblib.dump(model, 'f1_predictor.joblib')

# Visualization
plt.scatter(y_test, y_pred, alpha=0.6)
plt.xlabel("Actual Points")
plt.ylabel("Predicted Points")
plt.title("Predicted vs Actual Points - Random Forest Model")
plt.plot([0, 600], [0, 600], color='red', linestyle='--', label='Perfect Fit')  # perfect fit line
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
