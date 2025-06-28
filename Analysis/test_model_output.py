#!/usr/bin/env python3

import joblib
import numpy as np
import os

print("=== Testing Model Output ===")

# Load the model
model_path = "f1_position_predictor.joblib"
if os.path.exists(model_path):
    model = joblib.load(model_path)
    print(f"✅ Model loaded successfully")
    print(f"Model type: {type(model)}")
    print(f"Model classes: {getattr(model, 'classes_', 'No classes attribute')}")
    
    # Test prediction
    X_test = [[2024, 0, 3]]  # season=2024, team_encoded=0 (Red Bull), experience=3
    print(f"\nInput: {X_test}")
    
    pred = model.predict(X_test)
    print(f"Raw prediction: {pred}, type: {type(pred)}, element type: {type(pred[0])}")
    
    proba = model.predict_proba(X_test)
    print(f"Raw probabilities: {proba}")
    print(f"Probabilities shape: {proba.shape}")
    print(f"Max probability: {np.max(proba[0])}")
    
    # Convert to Python types
    predicted_position = int(pred[0])
    prediction_confidence = float(np.max(proba[0]))
    
    print(f"\nConverted values:")
    print(f"Predicted position: {predicted_position} (type: {type(predicted_position)})")
    print(f"Prediction confidence: {prediction_confidence} (type: {type(prediction_confidence)})")
    
    # Test multiple inputs
    print(f"\n=== Testing Multiple Inputs ===")
    test_cases = [
        [2024, 0, 3],  # Red Bull, experienced driver
        [2024, 1, 1],  # Mercedes, rookie
        [2024, 2, 5],  # Ferrari, very experienced
        [2023, 3, 2],  # McLaren, 2 years experience
    ]
    
    for i, test_case in enumerate(test_cases):
        pred = model.predict([test_case])
        proba = model.predict_proba([test_case])
        print(f"Test {i+1}: {test_case} -> Position: {int(pred[0])}, Confidence: {float(np.max(proba[0])):.3f}")

else:
    print(f"❌ Model file not found: {model_path}")
    
print("\n=== Testing Team Mapping ===")
team_mapping = {
    "Red Bull Racing": 0, "Mercedes": 1, "Ferrari": 2, "McLaren": 3,
    "Aston Martin": 4, "Alpine": 5, "Haas": 6, "RB": 7,
    "Williams": 8, "Kick Sauber": 9, "AlphaTauri": 7, "Alfa Romeo": 9
}

def get_team_name(team_encoded: int) -> str:
    """Convert team encoding back to team name"""
    for team, encoding in team_mapping.items():
        if encoding == team_encoded:
            return team
    return f"Team {team_encoded}"

for i in range(10):
    print(f"Team encoding {i} -> {get_team_name(i)}")
