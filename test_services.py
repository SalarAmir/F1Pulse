import requests
import json

def test_fastapi_directly():
    """Test FastAPI service directly"""
    print("=== Testing FastAPI Service ===")
    
    # Test health endpoint
    try:
        health_response = requests.get("http://localhost:8000/health")
        print(f"Health check status: {health_response.status_code}")
        print(f"Health response: {health_response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return False
    
    # Test prediction endpoint
    try:
        prediction_data = {
            "season": 2024,
            "team_encoded": 1,  # Mercedes
            "driver_name": "Lewis Hamilton",
            "race_name": "Azerbaijan Grand Prix"
        }
        
        print(f"\nTesting prediction with: {prediction_data}")
        
        response = requests.post("http://localhost:8000/predict", json=prediction_data)
        print(f"Prediction status: {response.status_code}")
        
        if response.ok:
            result = response.json()
            print(f"Prediction response:")
            print(json.dumps(result, indent=2))
            
            # Check key fields
            print(f"\nKey fields:")
            print(f"  - predicted_pts: {result.get('predicted_pts')}")
            print(f"  - is_historical: {result.get('is_historical')}")
            print(f"  - has historical_result: {result.get('historical_result') is not None}")
            
            if result.get('is_historical') and result.get('historical_result'):
                hist = result['historical_result']
                print(f"  - historical points: {hist.get('points')}")
                print(f"  - historical driver: {hist.get('driver')}")
            
            return True
        else:
            print(f"Prediction failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"Prediction test failed: {e}")
        return False

def test_spring_boot():
    """Test Spring Boot service"""
    print("\n=== Testing Spring Boot Service ===")
    
    try:
        prediction_data = {
            "season": 2024,
            "team_encoded": 1,  # Mercedes
            "driver_name": "Lewis Hamilton",
            "race_name": "Azerbaijan Grand Prix"
        }
        
        print(f"Testing Spring Boot with: {prediction_data}")
        
        response = requests.post("http://localhost:8080/api/predict", json=prediction_data)
        print(f"Spring Boot status: {response.status_code}")
        
        if response.ok:
            result = response.json()
            print(f"Spring Boot response:")
            print(json.dumps(result, indent=2))
            
            # Check key fields  
            print(f"\nKey fields:")
            print(f"  - predicted_pts: {result.get('predicted_pts')}")
            print(f"  - is_historical: {result.get('is_historical')}")
            print(f"  - has historical_result: {result.get('historical_result') is not None}")
            
            return True
        else:
            print(f"Spring Boot failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"Spring Boot test failed: {e}")
        return False

if __name__ == "__main__":
    print("F1 Prediction Service Tester")
    print("="*40)
    print("Note: CORS has been configured for FastAPI to allow frontend connections")
    print()
    
    fastapi_ok = test_fastapi_directly()
    spring_boot_ok = test_spring_boot()
    
    print(f"\n=== Summary ===")
    print(f"FastAPI: {'✅ OK' if fastapi_ok else '❌ Failed'}")
    print(f"Spring Boot: {'✅ OK' if spring_boot_ok else '❌ Failed'}")
    
    if not fastapi_ok:
        print("\n⚠️  FastAPI is not responding. Make sure to:")
        print("   1. cd to Analysis directory")
        print("   2. Run: python -m uvicorn main:app --reload --port 8000")
        print("   3. CORS middleware has been added to allow frontend connections")
    
    if not spring_boot_ok:
        print("\n⚠️  Spring Boot is not responding. Make sure to:")
        print("   1. cd to demo/demo directory") 
        print("   2. Run: mvn spring-boot:run")
