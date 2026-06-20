package com.rentifity.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.math.BigDecimal;

public class PaymentRequest {

    @NotNull
    private Long bookingId;

    @NotBlank
    private String paymentMethod;

    private String paymentChannel;

    @NotNull
    private BigDecimal amount;

    private String proofOfPayment;

    public PaymentRequest() {
    }

    public PaymentRequest(Long bookingId, String paymentMethod, String paymentChannel, BigDecimal amount, String proofOfPayment) {
        this.bookingId = bookingId;
        this.paymentMethod = paymentMethod;
        this.paymentChannel = paymentChannel;
        this.amount = amount;
        this.proofOfPayment = proofOfPayment;
    }

    public Long getBookingId() { return bookingId; }
    public void setBookingId(Long bookingId) { this.bookingId = bookingId; }

    public String getPaymentMethod() { return paymentMethod; }
    public void setPaymentMethod(String paymentMethod) { this.paymentMethod = paymentMethod; }

    public String getPaymentChannel() { return paymentChannel; }
    public void setPaymentChannel(String paymentChannel) { this.paymentChannel = paymentChannel; }

    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }

    public String getProofOfPayment() { return proofOfPayment; }
    public void setProofOfPayment(String proofOfPayment) { this.proofOfPayment = proofOfPayment; }
}
