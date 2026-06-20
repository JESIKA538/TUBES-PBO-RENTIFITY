package com.rentifity.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class BookingRequest {

    @NotNull
    private Long carId;

    @NotBlank
    private String startDate;

    @NotBlank
    private String endDate;

    private String notes;

    private String deliveryOption;
    private String deliveryAddress;

    public BookingRequest() {
    }

    public BookingRequest(Long carId, String startDate, String endDate, String notes, String deliveryOption, String deliveryAddress) {
        this.carId = carId;
        this.startDate = startDate;
        this.endDate = endDate;
        this.notes = notes;
        this.deliveryOption = deliveryOption;
        this.deliveryAddress = deliveryAddress;
    }

    public Long getCarId() { return carId; }
    public void setCarId(Long carId) { this.carId = carId; }

    public String getStartDate() { return startDate; }
    public void setStartDate(String startDate) { this.startDate = startDate; }

    public String getEndDate() { return endDate; }
    public void setEndDate(String endDate) { this.endDate = endDate; }

    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }

    public String getDeliveryOption() { return deliveryOption; }
    public void setDeliveryOption(String deliveryOption) { this.deliveryOption = deliveryOption; }

    public String getDeliveryAddress() { return deliveryAddress; }
    public void setDeliveryAddress(String deliveryAddress) { this.deliveryAddress = deliveryAddress; }
}
