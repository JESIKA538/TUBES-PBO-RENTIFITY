package com.rentifity.controller;

import com.rentifity.dto.request.CarRequest;
import com.rentifity.model.Car;
import com.rentifity.model.User;
import com.rentifity.security.CustomUserDetailsService;
import com.rentifity.service.CarService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/cars")
public class CarController {

    @Autowired
    private CarService carService;

    @Autowired
    private CustomUserDetailsService customUserDetailsService;

    private User getCurrentUser(Authentication authentication) {
        return customUserDetailsService.getUserByEmail(authentication.getName());
    }

    @GetMapping
    public ResponseEntity<List<Car>> index(
            @RequestParam(required = false) String status,
            @RequestParam(required = false) String search,
            @RequestParam(required = false) String type) {
        return ResponseEntity.ok(carService.getAllCars(status, search, type));
    }

    @GetMapping("/{id}")
    public ResponseEntity<Car> show(@PathVariable Long id) {
        return ResponseEntity.ok(carService.getCarById(id));
    }

    @PostMapping
    public ResponseEntity<Car> store(@Valid @RequestBody CarRequest request, Authentication auth) {
        User user = getCurrentUser(auth);
        if (!user.getRole().equals("admin")) {
            throw new RuntimeException("Forbidden");
        }
        return ResponseEntity.status(HttpStatus.CREATED).body(carService.createCar(request));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Car> update(@PathVariable Long id, @RequestBody CarRequest request, Authentication auth) {
        User user = getCurrentUser(auth);
        if (!user.getRole().equals("admin")) {
            throw new RuntimeException("Forbidden");
        }
        return ResponseEntity.ok(carService.updateCar(id, request));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Map<String, String>> destroy(@PathVariable Long id, Authentication auth) {
        User user = getCurrentUser(auth);
        if (!user.getRole().equals("admin")) {
            throw new RuntimeException("Forbidden");
        }
        carService.deleteCar(id);
        return ResponseEntity.ok(Map.of("message", "Mobil berhasil dihapus"));
    }
}
