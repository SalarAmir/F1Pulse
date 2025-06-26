package com.f1data.backend.controller;

import com.f1data.backend.model.Driver;
import com.f1data.backend.service.DriverService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/drivers")
@CrossOrigin
public class DriverController {

    private final DriverService driverService;

    public DriverController(DriverService driverService) {
        this.driverService = driverService;
    }

    @GetMapping
    public List<Driver> getAllDrivers() {
        return driverService.getAllDrivers();
    }

    @PostMapping("/import")
    public String importDrivers(@RequestBody List<Driver> drivers) {
        driverService.saveAll(drivers);
        return "✅ Imported successfully!";
    }
}
