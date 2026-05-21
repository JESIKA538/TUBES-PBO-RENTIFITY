package com.rentifity.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PaymentRequest {

    @NotNull
    private Long bookingId;

    @NotBlank
    private String paymentMethod;

    @NotNull
    private BigDecimal amount;

    private String proofOfPayment;
}
