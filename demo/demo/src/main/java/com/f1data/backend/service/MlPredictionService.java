package com.f1data.backend.service;

import com.f1data.backend.dto.PredictionRequest;
import com.f1data.backend.dto.PredictionResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class MlPredictionService {

    private final WebClient webClient;

    public MlPredictionService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.baseUrl("http://localhost:8000").build(); // FastAPI base URL
    }

    public double getPrediction(int season, int teamEncoded) {
        PredictionResponse response = getFullPrediction(season, teamEncoded, null, null);
        return response.getPredictedPosition(); // Return position as double for backward compatibility
    }
    
    public PredictionResponse getFullPrediction(int season, int teamEncoded, String driverName, String raceName) {
        return getFullPrediction(season, teamEncoded, driverName, raceName, 3); // Default 3 years experience
    }
    
    public PredictionResponse getFullPrediction(int season, int teamEncoded, String driverName, String raceName, int driverExperience) {
        PredictionRequest request = new PredictionRequest(season, teamEncoded, driverName, raceName, driverExperience);

        try {
            System.out.println("Calling FastAPI with: season=" + season + ", teamEncoded=" + teamEncoded + 
                             ", driver=" + driverName + ", race=" + raceName + ", experience=" + driverExperience);
            
            PredictionResponse response = webClient.post()
                    .uri("/predict")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(PredictionResponse.class)
                    .block();

            if (response != null) {
                System.out.println("FastAPI response received: predictedPosition=P" + response.getPredictedPosition() + 
                                 ", confidence=" + response.getPredictionConfidence() +
                                 ", isHistorical=" + response.isHistorical() + 
                                 ", hasHistoricalResult=" + (response.getHistoricalResult() != null));
                
                // Ensure all fields are properly set
                response.setSeason(season);
                response.setDriverName(driverName);
                response.setRaceName(raceName);
                return response;
            } else {
                System.err.println("FastAPI returned null response");
            }
        } catch (Exception e) {
            System.err.println("Error calling FastAPI: " + e.getMessage());
            e.printStackTrace();
        }

        System.out.println("Creating fallback response");
        // Create fallback response
        PredictionResponse fallback = new PredictionResponse(20); // Default to P20 (last place)
        fallback.setSeason(season);
        fallback.setDriverName(driverName);
        fallback.setRaceName(raceName);
        fallback.setIsHistorical(false); // Default to not historical if FastAPI fails
        return fallback;
    }

    public int getPredictedPosition(int season, int teamEncoded, String driverName, String raceName) {
        PredictionResponse response = getFullPrediction(season, teamEncoded, driverName, raceName);
        return response.getPredictedPosition();
    }

    public boolean testConnection() {
        try {
            String response = webClient.get()
                    .uri("/health")
                    .retrieve()
                    .bodyToMono(String.class)
                    .block();
            System.out.println("FastAPI health check: " + response);
            return response != null;
        } catch (Exception e) {
            System.err.println("FastAPI connection test failed: " + e.getMessage());
            return false;
        }
    }
}
