#!/usr/bin/env python3
"""
Test script to verify the F1 Pulse enhanced frontend works with FastAPI backend
"""

import requests
import json
import time
from datetime import datetime

# Test configuration
FASTAPI_URL = "http://localhost:8000"
TEST_PREDICTIONS = [
    {
        "season": 2024,
        "team_encoded": 0,  # Red Bull
        "driver_name": "Max Verstappen",
        "race_name": "Monaco Grand Prix",
        "driver_experience": 10
    },
    {
        "season": 2024,
        "team_encoded": 1,  # Mercedes
        "driver_name": "Lewis Hamilton", 
        "race_name": "British Grand Prix",
        "driver_experience": 17
    },
    {
        "season": 2024,
        "team_encoded": 2,  # Ferrari
        "driver_name": "Charles Leclerc",
        "race_name": "Italian Grand Prix", 
        "driver_experience": 6
    },
    {
        "season": 2025,  # Future prediction
        "team_encoded": 3,  # McLaren
        "driver_name": "Lando Norris",
        "race_name": "Las Vegas Grand Prix",
        "driver_experience": 5
    }
]

def test_fastapi_health():
    """Test if FastAPI backend is running"""
    try:
        response = requests.get(f"{FASTAPI_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ FastAPI backend is running")
            return True
        else:
            print(f"❌ FastAPI health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to FastAPI backend: {e}")
        return False

def test_prediction_endpoint(test_data):
    """Test a single prediction request"""
    try:
        print(f"\n🧪 Testing prediction for {test_data['driver_name']} at {test_data['race_name']}")
        
        response = requests.post(
            f"{FASTAPI_URL}/predict",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction successful!")
            print(f"   Predicted Position: P{result.get('predicted_position', 'Unknown')}")
            print(f"   Confidence: {(result.get('prediction_confidence', 0) * 100):.1f}%")
            
            if result.get('is_historical'):
                print(f"   Historical Result: P{result.get('historical_result', {}).get('position', 'N/A')}")
                print(f"   This is historical data for {test_data['season']}")
            else:
                print(f"   This is a future prediction for {test_data['season']}")
                
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_cors_headers():
    """Test CORS headers for frontend compatibility"""
    try:
        # Test preflight request
        response = requests.options(
            f"{FASTAPI_URL}/predict",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        cors_headers = {
            "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
            "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
            "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers")
        }
        
        print(f"\n🔍 CORS Headers Check:")
        for header, value in cors_headers.items():
            if value:
                print(f"   ✅ {header}: {value}")
            else:
                print(f"   ❌ {header}: Missing")
                
        return all(cors_headers.values())
        
    except requests.exceptions.RequestException as e:
        print(f"❌ CORS test failed: {e}")
        return False

def run_frontend_compatibility_test():
    """Run complete frontend compatibility test"""
    print("🏎️ F1 Pulse Frontend Compatibility Test")
    print("=" * 50)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Backend health
    if not test_fastapi_health():
        print("\n❌ Cannot proceed - FastAPI backend is not accessible")
        return False
    
    # Test 2: CORS compatibility
    cors_ok = test_cors_headers()
    if not cors_ok:
        print("\n⚠️  CORS issues detected - frontend may have connection problems")
    
    # Test 3: Prediction endpoints
    success_count = 0
    for i, test_data in enumerate(TEST_PREDICTIONS, 1):
        print(f"\n--- Test {i}/{len(TEST_PREDICTIONS)} ---")
        if test_prediction_endpoint(test_data):
            success_count += 1
        time.sleep(1)  # Brief delay between tests
    
    # Summary
    print(f"\n🏁 Test Summary:")
    print(f"   Successful predictions: {success_count}/{len(TEST_PREDICTIONS)}")
    print(f"   Success rate: {(success_count/len(TEST_PREDICTIONS)*100):.1f}%")
    
    if success_count == len(TEST_PREDICTIONS):
        print("✅ All tests passed! Frontend should work perfectly with the backend.")
    elif success_count > 0:
        print("⚠️  Some tests failed. Check the backend logs for issues.")
    else:
        print("❌ All tests failed. Backend may not be working correctly.")
    
    return success_count > 0

def main():
    """Main test function"""
    try:
        success = run_frontend_compatibility_test()
        exit_code = 0 if success else 1
        
        print(f"\n{'='*50}")
        if success:
            print("🎉 Frontend compatibility test completed successfully!")
            print("You can now start the React frontend with: npm run dev")
        else:
            print("💥 Frontend compatibility test failed!")
            print("Please check the FastAPI backend is running on localhost:8000")
        
        return exit_code
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
