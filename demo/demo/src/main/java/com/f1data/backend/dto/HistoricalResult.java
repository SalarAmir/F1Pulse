package com.f1data.backend.dto;

public class HistoricalResult {
    private Integer position;
    private Double points;
    private String driver;
    private String team;
    private int season;

    // Constructors
    public HistoricalResult() {}

    public HistoricalResult(Integer position, Double points, String driver, String team, int season) {
        this.position = position;
        this.points = points;
        this.driver = driver;
        this.team = team;
        this.season = season;
    }

    // Getters and Setters
    public Integer getPosition() {
        return position;
    }

    public void setPosition(Integer position) {
        this.position = position;
    }

    public Double getPoints() {
        return points;
    }

    public void setPoints(Double points) {
        this.points = points;
    }

    public String getDriver() {
        return driver;
    }

    public void setDriver(String driver) {
        this.driver = driver;
    }

    public String getTeam() {
        return team;
    }

    public void setTeam(String team) {
        this.team = team;
    }

    public int getSeason() {
        return season;
    }

    public void setSeason(int season) {
        this.season = season;
    }
}
