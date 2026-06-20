package com.rentifity.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "payments")
public class Payment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "payment_method")
    private String paymentMethod;

    @Column(name = "payment_channel")
    private String paymentChannel;

    @Column(name = "billing_code")
    private String billingCode;

    @Column(precision = 15, scale = 2)
    private BigDecimal amount;

    private String status = "pending";

    @Column(name = "proof_of_payment", columnDefinition = "LONGTEXT")
    private String proofOfPayment;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "booking_id")
    @JsonIgnoreProperties({"payments"})
    private Booking booking;

    public Payment() {
    }

    public Payment(Long id, String paymentMethod, String paymentChannel, String billingCode, BigDecimal amount, String status, String proofOfPayment, LocalDateTime createdAt, LocalDateTime updatedAt, Booking booking) {
        this.id = id;
        this.paymentMethod = paymentMethod;
        this.paymentChannel = paymentChannel;
        this.billingCode = billingCode;
        this.amount = amount;
        if (status != null) this.status = status;
        this.proofOfPayment = proofOfPayment;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
        this.booking = booking;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getPaymentMethod() { return paymentMethod; }
    public void setPaymentMethod(String paymentMethod) { this.paymentMethod = paymentMethod; }

    public String getPaymentChannel() { return paymentChannel; }
    public void setPaymentChannel(String paymentChannel) { this.paymentChannel = paymentChannel; }

    public String getBillingCode() { return billingCode; }
    public void setBillingCode(String billingCode) { this.billingCode = billingCode; }

    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public String getProofOfPayment() { return proofOfPayment; }
    public void setProofOfPayment(String proofOfPayment) { this.proofOfPayment = proofOfPayment; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }

    public Booking getBooking() { return booking; }
    public void setBooking(Booking booking) { this.booking = booking; }
}
