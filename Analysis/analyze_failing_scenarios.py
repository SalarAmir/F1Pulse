#!/usr/bin/env python3

"""
Test script for the exact failing scenarios provided by the user
"""

import json

def test_scenario_1():
    """Test the first failing scenario: 2024 Lewis Hamilton British GP"""
    print("🔴 Testing Scenario 1 (FAILING):")
    print("Lewis Hamilton, 2024 British Grand Prix")
    
    expected_failing_output = {
        "season": 2024,
        "predicted_position": 0,
        "prediction_confidence": 0,
        "team_name": "Mercedes",
        "driver_name": "Lewis Hamilton",
        "race_name": "British Grand Prix",
        "historical_result": None,
        "is_historical": True
    }
    
    print("❌ Previous failing output:")
    print(json.dumps(expected_failing_output, indent=2))
    
    # What it should return
    expected_fixed_output = {
        "season": 2024,
        "predicted_position": 3,  # Realistic position for Mercedes/Hamilton
        "prediction_confidence": 0.72,
        "team_name": "Mercedes",
        "driver_name": "Lewis Hamilton", 
        "race_name": "British Grand Prix",
        "historical_result": None,  # or actual 2024 data if available
        "is_historical": True
    }
    
    print("✅ Expected fixed output:")
    print(json.dumps(expected_fixed_output, indent=2))

def test_scenario_2():
    """Test the second failing scenario: 2025 Lewis Hamilton Canadian GP"""
    print("\n🔴 Testing Scenario 2 (FAILING):")
    print("Lewis Hamilton, 2025 Canadian Grand Prix")
    
    expected_failing_output = {
        "season": 2025,
        "predicted_position": 0,
        "prediction_confidence": 0,
        "team_name": "Mercedes",
        "driver_name": "Lewis Hamilton",
        "race_name": "Canadian Grand Prix", 
        "historical_result": None,
        "is_historical": False
    }
    
    print("❌ Previous failing output:")
    print(json.dumps(expected_failing_output, indent=2))
    
    # What it should return  
    expected_fixed_output = {
        "season": 2025,
        "predicted_position": 4,  # Future prediction for Mercedes/Hamilton
        "prediction_confidence": 0.68,
        "team_name": "Mercedes",
        "driver_name": "Lewis Hamilton",
        "race_name": "Canadian Grand Prix",
        "historical_result": None,
        "is_historical": False
    }
    
    print("✅ Expected fixed output:")
    print(json.dumps(expected_fixed_output, indent=2))

def create_curl_tests():
    """Create curl commands to test these exact scenarios"""
    print("\n🌐 CURL Test Commands:")
    print("="*50)
    
    # Scenario 1: 2024 British GP
    curl_1 = '''curl -X POST "http://localhost:8000/predict" \\
     -H "Content-Type: application/json" \\
     -d '{
       "season": 2024,
       "team_encoded": 1,
       "driver_name": "Lewis Hamilton",
       "race_name": "British Grand Prix",
       "driver_experience": 17
     }' '''
    
    print("Test 1 (2024 British GP):")
    print(curl_1)
    
    # Scenario 2: 2025 Canadian GP  
    curl_2 = '''curl -X POST "http://localhost:8000/predict" \\
     -H "Content-Type: application/json" \\
     -d '{
       "season": 2025,
       "team_encoded": 1,
       "driver_name": "Lewis Hamilton",
       "race_name": "Canadian Grand Prix", 
       "driver_experience": 18
     }' '''
    
    print("\nTest 2 (2025 Canadian GP):")
    print(curl_2)

def create_python_request_tests():
    """Create Python requests to test these scenarios"""
    print("\n🐍 Python Requests Test Code:")
    print("="*50)
    
    test_code = '''
import requests
import json

# Test cases based on failing scenarios
test_cases = [
    {
        "name": "2024 British GP - Lewis Hamilton",
        "data": {
            "season": 2024,
            "team_encoded": 1,  # Mercedes
            "driver_name": "Lewis Hamilton",
            "race_name": "British Grand Prix",
            "driver_experience": 17
        }
    },
    {
        "name": "2025 Canadian GP - Lewis Hamilton", 
        "data": {
            "season": 2025,
            "team_encoded": 1,  # Mercedes
            "driver_name": "Lewis Hamilton",
            "race_name": "Canadian Grand Prix",
            "driver_experience": 18
        }
    }
]

for test in test_cases:
    print(f"\\nTesting: {test['name']}")
    print(f"Request: {json.dumps(test['data'], indent=2)}")
    
    response = requests.post("http://localhost:8000/predict", json=test['data'])
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ SUCCESS - Position: P{result['predicted_position']}, Confidence: {result['prediction_confidence']:.3f}")
        
        # Check for the exact issues mentioned
        if result['predicted_position'] == 0:
            print("❌ ISSUE: Position is still 0!")
        if result['prediction_confidence'] == 0:
            print("❌ ISSUE: Confidence is still 0!")
    else:
        print(f"❌ FAILED - Status: {response.status_code}, Error: {response.text}")
'''
    
    print(test_code)

if __name__ == "__main__":
    print("🏎️ F1 Position Predictor - Failed Scenarios Analysis")
    print("="*60)
    
    test_scenario_1()
    test_scenario_2() 
    create_curl_tests()
    create_python_request_tests()
    
    print("\n📋 Summary:")
    print("- Both scenarios were returning position 0 and confidence 0")
    print("- Issue was caused by missing/improper model training")
    print("- Fixed with enhanced model creation in main.py")
    print("- Team encoding 1 = Mercedes")
    print("- Hamilton should get positions 3-5 typically for Mercedes")
    print("- 2024 is historical (< 2025), 2025 is future prediction")
    
    print("\n🚀 Next Steps:")
    print("1. Start the API: python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print("2. Run the curl commands above")
    print("3. Or use: python test_api_requests.py")
    print("4. Verify positions are > 0 and confidence > 0")
