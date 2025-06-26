package com.f1data.backend.service;


import com.f1data.backend.model.Driver;
import com.f1data.backend.repository.DriverRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class DriverService {
    private final DriverRepository driverRepository;

    public DriverService(DriverRepository driverRepository) {
        this.driverRepository = driverRepository;
    }

    public List<Driver> getAllDrivers() {
        return driverRepository.findAll();
    }

    public void saveAll(List<Driver> drivers) {
        driverRepository.saveAll(drivers);
    }
}