// Updated React service to call FastAPI directly instead of Spring Boot

// Before (calling Spring Boot):
// const API_BASE_URL = 'http://localhost:8080/api';

// After (calling FastAPI directly):
const API_BASE_URL = 'http://localhost:8080/api';  // FastAPI now runs on 8080

class F1PredictionService {
  static async predictPosition(predictionData) {
    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Optional: Add auth token if needed
          // 'Authorization': 'Bearer demo-token'
        },
        body: JSON.stringify(predictionData)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Prediction request failed:', error);
      throw error;
    }
  }

  static async getTeams() {
    try {
      const response = await fetch(`${API_BASE_URL}/teams`);
      const result = await response.json();
      return result.data.teams;  // Enhanced API returns wrapped data
    } catch (error) {
      console.error('Teams request failed:', error);
      throw error;
    }
  }

  static async getHistoricalData(season) {
    try {
      const response = await fetch(`${API_BASE_URL}/historical/${season}`);
      const result = await response.json();
      return result.data;
    } catch (error) {
      console.error('Historical data request failed:', error);
      throw error;
    }
  }

  static async getHealthStatus() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      const result = await response.json();
      return result.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }
}

export default F1PredictionService;
