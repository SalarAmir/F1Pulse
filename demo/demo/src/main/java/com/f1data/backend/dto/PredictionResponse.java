package com.f1data.backend.dto;

public class PredictionResponse {
    private double predicted_pts;

    // Constructors
    public PredictionResponse() {}
    
    public PredictionResponse(double predicted_pts) {
        this.predicted_pts = predicted_pts;
    }

    // Getters and Setters
    public double getPredicted_pts() {
        return predicted_pts;
    }

    public void setPredicted_pts(double predicted_pts) {
        this.predicted_pts = predicted_pts;
    }
}
