import requests
import json

# Test the position prediction API
API_BASE = "http://localhost:8000"

def test_position_prediction():
    """Test the position prediction endpoint"""
    
    print("🧪 Testing F1 Position Prediction API")
    print("=" * 50)
    
    # Test data
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
            "race_name": "British GP",
            "driver_experience": 15
        },
        {
            "season": 2022,
            "team_encoded": 2,  # Ferrari
            "driver_name": "Charles Leclerc",
            "race_name": "Italian GP",
            "driver_experience": 5
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🏎️ Test Case {i}: {test_case['driver_name']} - {test_case['race_name']}")
        print(f"   Season: {test_case['season']}")
        print(f"   Team: {test_case['team_encoded']}")
        print(f"   Experience: {test_case['driver_experience']} years")
        
        try:
            response = requests.post(f"{API_BASE}/predict", json=test_case)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ SUCCESS")
                print(f"   📊 Predicted Position: P{result['predicted_position']}")
                print(f"   🎯 Confidence: {result['prediction_confidence']:.3f}")
                print(f"   📅 Is Historical: {result['is_historical']}")
                
                if result['historical_result']:
                    hist = result['historical_result']
                    print(f"   📈 Historical Result: P{hist['position']} ({hist['points']} pts)")
                    print(f"   🏁 Driver: {hist['driver']}")
                else:
                    print(f"   📈 No historical data available")
                    
            else:
                print(f"   ❌ ERROR: {response.status_code}")
                print(f"   {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ CONNECTION ERROR: API server not running")
            print(f"   💡 Please start the server with: uvicorn main:app --reload")
            break
        except Exception as e:
            print(f"   ❌ ERROR: {e}")

def test_api_info():
    """Test basic API endpoints"""
    print(f"\n🔍 Testing API Information Endpoints")
    print("-" * 30)
    
    endpoints = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/teams", "Team mappings"),
        ("/debug/data", "Debug data info")
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{API_BASE}{endpoint}")
            if response.status_code == 200:
                print(f"✅ {description}: {response.status_code}")
                if endpoint == "/":
                    data = response.json()
                    print(f"   API: {data.get('message', 'N/A')}")
                elif endpoint == "/teams":
                    data = response.json()
                    teams = data.get('teams', {})
                    print(f"   Available teams: {len(teams)}")
            else:
                print(f"❌ {description}: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ {description}: Connection failed")
            return False
        except Exception as e:
            print(f"❌ {description}: {e}")
    
    return True

if __name__ == "__main__":
    # Test basic endpoints first
    if test_api_info():
        # If basic endpoints work, test predictions
        test_position_prediction()
    
    print(f"\n🏁 Testing complete!")
    print(f"💡 To start the API server: uvicorn main:app --reload")
