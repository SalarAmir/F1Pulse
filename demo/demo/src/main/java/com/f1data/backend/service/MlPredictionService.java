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
        PredictionRequest request = new PredictionRequest(season, teamEncoded);

        PredictionResponse response = webClient.post()
                .uri("/predict")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(PredictionResponse.class)
                .block();

        return response != null ? response.getPredicted_pts() : -1;
    }
}
