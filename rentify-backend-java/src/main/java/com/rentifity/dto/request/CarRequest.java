package com.rentifity.dto.request;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@Data
@NoArgsConstructor
@AllArgsConstructor
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
}
