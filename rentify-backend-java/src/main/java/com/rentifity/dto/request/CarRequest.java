package com.rentifity.dto.request;

import java.math.BigDecimal;

public class CarRequest {

    private String name;

    private String brand;

    private String type;

    private String transmission;

    private String fuelType;

    private BigDecimal pricePerDay;

    private String status;

    private String imageUrl;

    private String description;

    public CarRequest() {
    }

    public CarRequest(String name, String brand, String type, String transmission, String fuelType, BigDecimal pricePerDay, String status, String imageUrl, String description) {
        this.name = name;
        this.brand = brand;
        this.type = type;
        this.transmission = transmission;
        this.fuelType = fuelType;
        this.pricePerDay = pricePerDay;
        this.status = status;
        this.imageUrl = imageUrl;
        this.description = description;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getBrand() { return brand; }
    public void setBrand(String brand) { this.brand = brand; }

    public String getType() { return type; }
    public void setType(String type) { this.type = type; }

    public String getTransmission() { return transmission; }
    public void setTransmission(String transmission) { this.transmission = transmission; }

    public String getFuelType() { return fuelType; }
    public void setFuelType(String fuelType) { this.fuelType = fuelType; }

    public BigDecimal getPricePerDay() { return pricePerDay; }
    public void setPricePerDay(BigDecimal pricePerDay) { this.pricePerDay = pricePerDay; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public String getImageUrl() { return imageUrl; }
    public void setImageUrl(String imageUrl) { this.imageUrl = imageUrl; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}
