import requests
import json

def test_fastapi_2024():
    """Test FastAPI with 2024 data specifically"""
    print("=== Testing FastAPI for 2024 Lewis Hamilton ===")
    
    try:
        # Test the exact case that's failing
        prediction_data = {
            "season": 2024,
            "team_encoded": 1,  # Mercedes
            "driver_name": "Lewis Hamilton",
            "race_name": "Azerbaijan Grand Prix"
        }
        
        response = requests.post("http://localhost:8000/predict", json=prediction_data)
        print(f"Status: {response.status_code}")
        
        if response.ok:
            result = response.json()
            print("FastAPI Response:")
            print(json.dumps(result, indent=2))
            
            # Check the specific issue
            is_historical = result.get('is_historical')
            predicted_pts = result.get('predicted_pts')
            
            print(f"\n🔍 Analysis:")
            print(f"  - Season: {result.get('season')} (should be 2024)")
            print(f"  - is_historical: {is_historical} (should be TRUE for 2024)")
            print(f"  - predicted_pts: {predicted_pts} (should be > 0)")
            print(f"  - has historical_result: {result.get('historical_result') is not None}")
            
            if is_historical:
                print("  ✅ Correctly identified as historical")
            else:
                print("  ❌ PROBLEM: 2024 should be historical!")
                
            return result
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def test_debug_endpoint():
    """Test the debug endpoint to see available data"""
    print("\n=== Testing Debug Endpoint ===")
    
    try:
        response = requests.get("http://localhost:8000/debug/data")
        print(f"Debug status: {response.status_code}")
        
        if response.ok:
            result = response.json()
            print("Debug response:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Debug failed: {response.text}")
            
    except Exception as e:
        print(f"Debug request failed: {e}")

if __name__ == "__main__":
    print("FastAPI 2024 Historical Data Test")
    print("="*40)
    
    # Test health first
    try:
        health = requests.get("http://localhost:8000/health")
        print(f"Health: {health.status_code} - {health.json() if health.ok else health.text}")
    except Exception as e:
        print(f"Health check failed: {e}")
        print("FastAPI might not be running!")
        exit(1)
    
    # Test the specific 2024 case
    result = test_fastapi_2024()
    
    # Test debug endpoint
    test_debug_endpoint()
    
    print(f"\n=== Summary ===")
    if result:
        is_correct = result.get('is_historical') == True
        print(f"2024 historical detection: {'✅ WORKING' if is_correct else '❌ BROKEN'}")
    else:
        print("❌ FastAPI request failed")
