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
    public PredictionResponse predictPointsGet(@RequestParam int season, @RequestParam int teamEncoded) {
        logger.info("GET request - Season: {}, TeamEncoded: {}", season, teamEncoded);
        double prediction = predictionService.getPrediction(season, teamEncoded);
        return new PredictionResponse(prediction);
    }
    
    // POST method for JSON body requests (recommended)
    @PostMapping
    public ResponseEntity<PredictionResponse> predictPointsPost(@RequestBody PredictionRequest request) {
        try {
            logger.info("POST request received - Season: {}, TeamEncoded: {}", request.getSeason(), request.getTeamEncoded());
            double prediction = predictionService.getPrediction(request.getSeason(), request.getTeamEncoded());
            return ResponseEntity.ok(new PredictionResponse(prediction));
        } catch (Exception e) {
            logger.error("Error processing prediction request", e);
            return ResponseEntity.internalServerError().build();
        }
    }
}
