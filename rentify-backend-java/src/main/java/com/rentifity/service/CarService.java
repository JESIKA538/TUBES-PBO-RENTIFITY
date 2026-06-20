package com.rentifity.service;

import com.rentifity.dto.request.CarRequest;
import com.rentifity.exception.ResourceNotFoundException;
import com.rentifity.model.Car;
import com.rentifity.repository.CarRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CarService {

    @Autowired
    private CarRepository carRepository;

    public List<Car> getAllCars(String status, String search, String type) {
        if (status != null && status.isBlank()) status = null;
        if (search != null && search.isBlank()) search = null;
        if (type != null && type.isBlank()) type = null;

        return carRepository.findWithFilters(status, type, search);
    }

    public Car getCarById(Long id) {
        return carRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Mobil tidak ditemukan"));
    }

    public Car createCar(CarRequest req) {
        Car car = new Car();
        car.setName(req.getName());
        car.setBrand(req.getBrand());
        car.setType(req.getType());
        car.setTransmission(req.getTransmission());
        car.setFuelType(req.getFuelType());
        car.setPricePerDay(req.getPricePerDay());
        car.setStatus(req.getStatus());
        car.setImageUrl(req.getImageUrl());
        car.setDescription(req.getDescription());

        return carRepository.save(car);
    }

    public Car updateCar(Long id, CarRequest req) {
        Car car = carRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Mobil tidak ditemukan"));

        if (req.getName() != null) car.setName(req.getName());
        if (req.getBrand() != null) car.setBrand(req.getBrand());
        if (req.getType() != null) car.setType(req.getType());
        if (req.getTransmission() != null) car.setTransmission(req.getTransmission());
        if (req.getFuelType() != null) car.setFuelType(req.getFuelType());
        if (req.getPricePerDay() != null) car.setPricePerDay(req.getPricePerDay());
        if (req.getStatus() != null) car.setStatus(req.getStatus());
        if (req.getImageUrl() != null) car.setImageUrl(req.getImageUrl());
        if (req.getDescription() != null) car.setDescription(req.getDescription());

        return carRepository.save(car);
    }

    public void deleteCar(Long id) {
        Car car = carRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Mobil tidak ditemukan"));
        carRepository.delete(car);
    }
}
