import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our main module
import main

def test_specific_case():
    """Test the specific case that was showing position 0"""
    
    print("🧪 Testing Specific Position Prediction Case")
    print("=" * 50)
    
    # The problematic case from the user
    test_case = {
        "season": 2024,
        "team_encoded": 1,  # Mercedes
        "driver_name": "Lewis Hamilton",
        "race_name": "Australian Grand Prix",
        "driver_experience": 15  # Very experienced driver
    }
    
    print(f"🏎️ Test Case: {test_case['driver_name']} - {test_case['race_name']}")
    print(f"   Season: {test_case['season']}")
    print(f"   Team: Mercedes (encoded: {test_case['team_encoded']})")
    print(f"   Experience: {test_case['driver_experience']} years")
    
    try:
        # Create request object
        request = main.PredictRequest(**test_case)
        
        # Call prediction function directly
        response = main.predict_position(request)
        
        print(f"\n✅ PREDICTION SUCCESSFUL")
        print(f"📊 Predicted Position: P{response.predicted_position}")
        print(f"🎯 Confidence: {response.prediction_confidence:.3f} ({response.prediction_confidence*100:.1f}%)")
        print(f"🏁 Team: {response.team_name}")
        print(f"📅 Is Historical: {response.is_historical}")
        print(f"🔍 Season Classification: {'Historical' if response.is_historical else 'Future/Current'}")
        
        if response.historical_result:
            hist = response.historical_result
            print(f"\n📈 Historical Result Found:")
            print(f"   Position: P{hist.position}")
            print(f"   Points: {hist.points}")
            print(f"   Driver: {hist.driver}")
            print(f"   Team: {hist.team}")
        else:
            print(f"\n📈 No historical data found for this combination")
        
        # Verify the response is not the problematic one
        if response.predicted_position == 0:
            print(f"\n❌ ERROR: Still getting position 0!")
            return False
        elif response.prediction_confidence == 0:
            print(f"\n❌ ERROR: Still getting 0 confidence!")
            return False
        else:
            print(f"\n✅ SUCCESS: Valid prediction received!")
            return True
                
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_cases():
    """Test multiple cases to ensure consistent results"""
    
    print(f"\n🔄 Testing Multiple Cases")
    print("-" * 30)
    
    test_cases = [
        {"season": 2024, "team_encoded": 0, "driver_experience": 10, "driver_name": "Max Verstappen"},
        {"season": 2024, "team_encoded": 1, "driver_experience": 15, "driver_name": "Lewis Hamilton"},
        {"season": 2024, "team_encoded": 2, "driver_experience": 5, "driver_name": "Charles Leclerc"},
        {"season": 2024, "team_encoded": 8, "driver_experience": 2, "driver_name": "Logan Sargeant"},
        {"season": 2023, "team_encoded": 0, "driver_experience": 10, "driver_name": "Max Verstappen"},
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. {case['driver_name']} ({main.get_team_name(case['team_encoded'])}) - {case['season']}")
        
        try:
            request = main.PredictRequest(**case)
            response = main.predict_position(request)
            
            print(f"   → P{response.predicted_position} (conf: {response.prediction_confidence:.3f})")
            
            if response.predicted_position == 0 or response.prediction_confidence == 0:
                print(f"   ❌ Invalid prediction!")
            else:
                print(f"   ✅ Valid prediction")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def show_model_details():
    """Show details about the loaded model"""
    
    print(f"\n🤖 Model Details")
    print("-" * 20)
    
    try:
        model = main.model
        print(f"Model type: {type(model)}")
        print(f"Model classes: {model.classes_}")
        print(f"Number of classes: {len(model.classes_)}")
        print(f"Features expected: {main.model_info.get('features', 'Unknown')}")
        
        # Test a simple prediction
        import numpy as np
        test_input = np.array([[2024, 1, 10]])
        pred = model.predict(test_input)[0]
        prob = model.predict_proba(test_input)[0]
        conf = max(prob)
        
        print(f"\nDirect model test:")
        print(f"Input: {test_input[0]}")
        print(f"Prediction: P{pred}")
        print(f"Confidence: {conf:.3f}")
        
    except Exception as e:
        print(f"Error accessing model: {e}")

if __name__ == "__main__":
    print("🏎️ F1 Position Predictor - Debugging Issue")
    print("=" * 50)
    
    # Show model details
    show_model_details()
    
    # Test the specific problematic case
    success = test_specific_case()
    
    if success:
        # Test multiple cases
        test_multiple_cases()
        print(f"\n✅ All tests completed successfully!")
        print(f"🎯 The position prediction is now working correctly!")
    else:
        print(f"\n❌ Issue still exists - needs further debugging")
