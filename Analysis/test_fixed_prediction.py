#!/usr/bin/env python3

# Test the fixed prediction API
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔥 Testing Fixed Position Prediction")
print("="*50)

try:
    # Import the main app to trigger model creation
    from main import app, model, predict_position, PredictRequest
    
    print("✅ Main app imported successfully")
    print(f"✅ Model loaded: {model}")
    
    # Test cases that were failing
    test_cases = [
        {
            "season": 2024,
            "team_encoded": 1,  # Mercedes
            "driver_name": "Lewis Hamilton",
            "race_name": "British Grand Prix",
            "driver_experience": 17
        },
        {
            "season": 2025,
            "team_encoded": 1,  # Mercedes
            "driver_name": "Lewis Hamilton", 
            "race_name": "Canadian Grand Prix",
            "driver_experience": 18
        },
        {
            "season": 2024,
            "team_encoded": 0,  # Red Bull
            "driver_name": "Max Verstappen",
            "race_name": "Monaco GP",
            "driver_experience": 10
        },
        {
            "season": 2023,
            "team_encoded": 2,  # Ferrari
            "driver_name": "Charles Leclerc",
            "race_name": "Italian GP",
            "driver_experience": 7
        }
    ]
    
    print(f"\n🧪 Testing {len(test_cases)} cases:")
    print("-" * 50)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {case['driver_name']} ({case['season']})")
        print(f"Team encoding: {case['team_encoded']}, Experience: {case['driver_experience']}")
        
        # Create request
        request = PredictRequest(**case)
        
        # Get prediction
        try:
            response = predict_position(request)
            
            print(f"✅ RESULT:")
            print(f"   Predicted Position: P{response.predicted_position}")
            print(f"   Confidence: {response.prediction_confidence:.3f}")
            print(f"   Team: {response.team_name}")
            print(f"   Is Historical: {response.is_historical}")
            if response.historical_result:
                print(f"   Historical Result: P{response.historical_result.position}")
            
            # Check for zero values
            if response.predicted_position == 0:
                print(f"   ❌ ISSUE: Position is 0!")
            if response.prediction_confidence == 0.0:
                print(f"   ❌ ISSUE: Confidence is 0!")
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n✅ Testing completed!")
    
except Exception as e:
    print(f"❌ Failed to import or test: {e}")
    import traceback
    traceback.print_exc()
