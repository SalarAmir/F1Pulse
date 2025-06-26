package com.f1data.backend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class PredictionRequest {
    private int season;
    
    @JsonProperty("team_encoded") // Use snake_case to match FastAPI convention
    private int teamEncoded;

    // Constructors
    public PredictionRequest() {}
    public PredictionRequest(int season, int teamEncoded) {
        this.season = season;
        this.teamEncoded = teamEncoded;
    }

    // Getters and Setters
    public int getSeason() { return season; }
    public void setSeason(int season) { this.season = season; }

    public int getTeamEncoded() { return teamEncoded; }
    public void setTeamEncoded(int teamEncoded) { this.teamEncoded = teamEncoded; }
}

