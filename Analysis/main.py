from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI()

# Load your trained ML model (adjust path as needed)
model_path = "f1_predictor.joblib"
if not os.path.exists(model_path):
    print(f"❌ Model file '{model_path}' not found!")
    print("Please run read_data.py first to train and save the model.")
    exit(1)

model = joblib.load(model_path)
print(f"✅ Model loaded successfully from {model_path}")

class PredictRequest(BaseModel):
    season: int
    team_encoded: int  # Changed from position to team_encoded to match training data

class PredictResponse(BaseModel):
    predicted_pts: float

@app.post("/predict", response_model=PredictResponse)
def predict_points(request: PredictRequest):
    # Prepare input features in the same order as trained: [season, team_encoded]
    X = np.array([[request.season, request.team_encoded]])
    
    # Get prediction from the model
    predicted_pts = model.predict(X)[0]
    
    # Optional: constrain predicted points if needed (e.g., no negative)
    predicted_pts = max(predicted_pts, 0)
    
    return PredictResponse(predicted_pts=predicted_pts)

@app.get("/")
def root():
    return {
        "message": "F1 Points Predictor API", 
        "status": "running",
        "usage": "POST to /predict with JSON: {'season': int, 'team_encoded': int}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# To run the FastAPI app manually, use the command:
# uvicorn main:app --reload     