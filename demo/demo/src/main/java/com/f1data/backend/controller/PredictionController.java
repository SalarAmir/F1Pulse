// src/main/java/com/f1data/backend/controller/PredictionController.java
package com.f1data.backend.controller;

import com.f1data.backend.dto.PredictionRequest;
import com.f1data.backend.dto.PredictionResponse;
import com.f1data.backend.service.MlPredictionService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/predict")
@CrossOrigin(origins = "*") // Allow CORS for frontend access
public class PredictionController {
    private static final Logger logger = LoggerFactory.getLogger(PredictionController.class);
    private final MlPredictionService predictionService;

    public PredictionController(MlPredictionService predictionService) {
        this.predictionService = predictionService;
    }

    // GET method for simple query parameter access
    @GetMapping
    public PredictionResponse predictPositionGet(@RequestParam int season, @RequestParam int teamEncoded) {
        logger.info("GET request - Season: {}, TeamEncoded: {}", season, teamEncoded);
        PredictionResponse response = predictionService.getFullPrediction(season, teamEncoded, null, null);
        return response;
    }
    
    // POST method for JSON body requests with full data (recommended)
    @PostMapping
    public ResponseEntity<PredictionResponse> predictPositionPost(@RequestBody PredictionRequest request) {
        try {
            logger.info("POST request received - Season: {}, TeamEncoded: {}, Driver: {}, Race: {}, Experience: {}", 
                       request.getSeason(), request.getTeamEncoded(), request.getDriverName(), 
                       request.getRaceName(), request.getDriverExperience());
            
            // Test FastAPI connection first
            boolean isConnected = predictionService.testConnection();
            logger.info("FastAPI connection status: {}", isConnected);
            
            PredictionResponse response = predictionService.getFullPrediction(
                request.getSeason(), 
                request.getTeamEncoded(), 
                request.getDriverName(), 
                request.getRaceName(),
                request.getDriverExperience()
            );
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            logger.error("Error processing prediction request", e);
            return ResponseEntity.internalServerError().build();
        }
    }
}
