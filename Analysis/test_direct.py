import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our main module
import main

def test_position_prediction_direct():
    """Test position prediction directly without HTTP"""
    
    print("🧪 Testing Position Prediction (Direct)")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "season": 2024,
            "team_encoded": 0,  # Red Bull Racing
            "driver_name": "Max Verstappen",
            "race_name": "Monaco GP",
            "driver_experience": 10
        },
        {
            "season": 2023,
            "team_encoded": 1,  # Mercedes
            "driver_name": "Lewis Hamilton",
            "driver_experience": 15
        },
        {
            "season": 2022,
            "team_encoded": 8,  # Williams
            "driver_name": "Alex Albon",
            "driver_experience": 3
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🏎️ Test Case {i}: {test_case.get('driver_name', 'Unknown Driver')}")
        print(f"   Season: {test_case['season']}")
        print(f"   Team Code: {test_case['team_encoded']}")
        print(f"   Experience: {test_case['driver_experience']} years")
        
        try:
            # Create request object
            request = main.PredictRequest(**test_case)
            
            # Call prediction function directly
            response = main.predict_position(request)
            
            print(f"   ✅ SUCCESS")
            print(f"   📊 Predicted Position: P{response.predicted_position}")
            print(f"   🎯 Confidence: {response.prediction_confidence:.3f}")
            print(f"   🏁 Team: {response.team_name}")
            print(f"   📅 Is Historical: {response.is_historical}")
            
            if response.historical_result:
                hist = response.historical_result
                print(f"   📈 Historical Result: P{hist.position} ({hist.points} pts)")
                print(f"   🏁 Historical Driver: {hist.driver}")
            else:
                print(f"   📈 No historical data found")
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            import traceback
            traceback.print_exc()

def test_team_mappings():
    """Test team mapping functionality"""
    print(f"\n🏁 Testing Team Mappings")
    print("-" * 30)
    
    for team_name, team_code in main.team_mapping.items():
        converted_name = main.get_team_name(team_code)
        print(f"  {team_code}: {team_name} -> {converted_name}")

def test_model_info():
    """Test model and data loading"""
    print(f"\n🤖 Model & Data Information")
    print("-" * 30)
    
    print(f"  Model loaded: {hasattr(main, 'model')}")
    print(f"  Model info: {hasattr(main, 'model_info')}")
    print(f"  Historical data: {main.historical_data is not None}")
    
    if hasattr(main, 'model_info'):
        print(f"  Features: {main.model_info.get('features', 'N/A')}")
        print(f"  Model type: {main.model_info.get('model_type', 'N/A')}")
    
    if main.historical_data is not None:
        print(f"  Data shape: {main.historical_data.shape}")
        print(f"  Seasons available: {sorted(main.historical_data['season'].unique())}")

if __name__ == "__main__":
    print("🏎️ F1 Position Predictor - Direct Testing")
    print("=" * 50)
    
    # Test model and data info
    test_model_info()
    
    # Test team mappings
    test_team_mappings()
    
    # Test position predictions
    test_position_prediction_direct()
    
    print(f"\n✅ All tests completed!")
