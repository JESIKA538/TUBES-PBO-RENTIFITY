package com.rentifity.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

//ENKAPSULASI
@Entity
@Table(name = "cars")
public class Car {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    // SEMUA ATRIBUT DIDEKLARASIKAN DENGAN AKSES MODIFIER PRIVATE
    // UNTUK MENJAGA KEAMANAN DAN INTEGRITAS DATA
    private Long id;

    private String name;

    private String brand;

    private String type;

    private String transmission;

    @Column(name = "fuel_type")
    private String fuelType;

    @Column(name = "price_per_day", precision = 15, scale = 2)
    private BigDecimal pricePerDay;

    private String status = "available";

    @Column(name = "image_url", columnDefinition = "LONGTEXT")
    private String imageUrl;

    @Column(columnDefinition = "TEXT")
    private String description;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @OneToMany(mappedBy = "car")
    @JsonIgnore
    private List<Booking> bookings;

    //METHOD GETTER DAN SETTER UNTUK MENGAKSES DAN MEMODIFIKASI NILAI
    public Car() {
    }

    public Car(Long id, String name, String brand, String type, String transmission, String fuelType, BigDecimal pricePerDay, String status, String imageUrl, String description, LocalDateTime createdAt, LocalDateTime updatedAt, List<Booking> bookings) {
        this.id = id;
        this.name = name;
        this.brand = brand;
        this.type = type;
        this.transmission = transmission;
        this.fuelType = fuelType;
        this.pricePerDay = pricePerDay;
        if (status != null) this.status = status;
        this.imageUrl = imageUrl;
        this.description = description;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
        this.bookings = bookings;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

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

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }

    public List<Booking> getBookings() { return bookings; }
    public void setBookings(List<Booking> bookings) { this.bookings = bookings; }
}
