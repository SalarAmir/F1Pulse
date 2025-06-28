package com.f1data.backend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class PredictionRequest {
    private int season;
    
    @JsonProperty("team_encoded")
    private int teamEncoded;
    
    @JsonProperty("driver_name")
    private String driverName;
    
    @JsonProperty("race_name")
    private String raceName;
    
    @JsonProperty("driver_experience")
    private int driverExperience = 3; // Default to 3 years experience

    // Constructors
    public PredictionRequest() {}
    
    public PredictionRequest(int season, int teamEncoded) {
        this.season = season;
        this.teamEncoded = teamEncoded;
    }
    
    public PredictionRequest(int season, int teamEncoded, String driverName, String raceName) {
        this.season = season;
        this.teamEncoded = teamEncoded;
        this.driverName = driverName;
        this.raceName = raceName;
        this.driverExperience = 3; // Default
    }

    public PredictionRequest(int season, int teamEncoded, String driverName, String raceName, int driverExperience) {
        this.season = season;
        this.teamEncoded = teamEncoded;
        this.driverName = driverName;
        this.raceName = raceName;
        this.driverExperience = driverExperience;
    }

    // Getters and Setters
    public int getSeason() { return season; }
    public void setSeason(int season) { this.season = season; }

    public int getTeamEncoded() { return teamEncoded; }
    public void setTeamEncoded(int teamEncoded) { this.teamEncoded = teamEncoded; }
    
    public String getDriverName() { return driverName; }
    public void setDriverName(String driverName) { this.driverName = driverName; }
    
    public String getRaceName() { return raceName; }
    public void setRaceName(String raceName) { this.raceName = raceName; }
    
    public int getDriverExperience() { return driverExperience; }
    public void setDriverExperience(int driverExperience) { this.driverExperience = driverExperience; }
}

