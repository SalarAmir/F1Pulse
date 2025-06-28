#!/usr/bin/env python3

import requests
import json
import time

print("🌐 Testing F1 Position Prediction API")
print("="*50)

# Test if server is running
api_url = "http://localhost:8000"
test_url = f"{api_url}/health"

print(f"🔍 Checking if API is running at {api_url}")

try:
    response = requests.get(test_url, timeout=5)
    if response.status_code == 200:
        print("✅ API is running!")
    else:
        print(f"⚠️ API responded with status: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"❌ API not running or not accessible: {e}")
    print("Please start the API server first:")
    print("python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    exit(1)

# Test prediction endpoint
predict_url = f"{api_url}/predict"

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
    }
]

print(f"\n🧪 Testing prediction endpoint:")
print("-" * 50)

for i, test_case in enumerate(test_cases, 1):
    print(f"\nTest {i}: {test_case['driver_name']} ({test_case['season']})")
    print(f"Request: {json.dumps(test_case, indent=2)}")
    
    try:
        response = requests.post(predict_url, json=test_case, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response:")
            print(f"   Status: {response.status_code}")
            print(f"   Predicted Position: P{result.get('predicted_position', 'N/A')}")
            print(f"   Confidence: {result.get('prediction_confidence', 'N/A')}")
            print(f"   Team: {result.get('team_name', 'N/A')}")
            print(f"   Is Historical: {result.get('is_historical', 'N/A')}")
            
            # Check for issues
            if result.get('predicted_position') == 0:
                print(f"   ❌ ISSUE: Position is 0!")
            if result.get('prediction_confidence') == 0.0:
                print(f"   ❌ ISSUE: Confidence is 0!")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

print(f"\n✅ API testing completed!")
