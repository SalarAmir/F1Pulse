package com.f1data.backend.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;

public class PredictionResponse {
    @JsonProperty("predicted_position")
    private int predictedPosition;
    
    @JsonProperty("prediction_confidence")
    private double predictionConfidence;
    
    private int season;
    
    @JsonProperty("team_name")
    private String teamName;
    
    @JsonProperty("driver_name")
    private String driverName;
    
    @JsonProperty("race_name")
    private String raceName;
    
    @JsonProperty("historical_result")
    private HistoricalResult historicalResult;
    
    @JsonProperty("is_historical")
    private boolean isHistorical;

    // Constructors
    public PredictionResponse() {}
    
    public PredictionResponse(int predictedPosition) {
        this.predictedPosition = predictedPosition;
        this.predictionConfidence = 0.0;
    }
    
    public PredictionResponse(int predictedPosition, double predictionConfidence) {
        this.predictedPosition = predictedPosition;
        this.predictionConfidence = predictionConfidence;
    }

    // Getters and Setters - Using consistent camelCase naming
    public int getPredictedPosition() {
        return predictedPosition;
    }

    public void setPredictedPosition(int predictedPosition) {
        this.predictedPosition = predictedPosition;
    }
    
    public double getPredictionConfidence() {
        return predictionConfidence;
    }

    public void setPredictionConfidence(double predictionConfidence) {
        this.predictionConfidence = predictionConfidence;
    }

    public int getSeason() {
        return season;
    }

    public void setSeason(int season) {
        this.season = season;
    }

    public String getTeamName() {
        return teamName;
    }

    public void setTeamName(String teamName) {
        this.teamName = teamName;
    }

    public String getDriverName() {
        return driverName;
    }

    public void setDriverName(String driverName) {
        this.driverName = driverName;
    }

    public String getRaceName() {
        return raceName;
    }

    public void setRaceName(String raceName) {
        this.raceName = raceName;
    }

    public HistoricalResult getHistoricalResult() {
        return historicalResult;
    }

    public void setHistoricalResult(HistoricalResult historicalResult) {
        this.historicalResult = historicalResult;
    }

    @JsonIgnore
    public boolean isHistorical() {
        return isHistorical;
    }

    @JsonProperty("is_historical")
    public boolean getIsHistorical() {
        return isHistorical;
    }

    public void setIsHistorical(boolean isHistorical) {
        this.isHistorical = isHistorical;
    }
}
