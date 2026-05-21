package com.rentifity.controller;

import com.rentifity.dto.request.PaymentRequest;
import com.rentifity.model.Payment;
import com.rentifity.model.User;
import com.rentifity.security.CustomUserDetailsService;
import com.rentifity.service.PaymentService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class PaymentController {

    @Autowired
    private PaymentService paymentService;

    @Autowired
    private CustomUserDetailsService customUserDetailsService;

    private User getCurrentUser(Authentication authentication) {
        return customUserDetailsService.getUserByEmail(authentication.getName());
    }

    @GetMapping("/payments")
    public ResponseEntity<List<Payment>> index(Authentication auth) {
        User user = getCurrentUser(auth);
        return ResponseEntity.ok(paymentService.getAllPayments(user));
    }

    @PostMapping("/payments")
    public ResponseEntity<Payment> createPayment(@Valid @RequestBody PaymentRequest request, Authentication auth) {
        User user = getCurrentUser(auth);
        return ResponseEntity.status(HttpStatus.CREATED).body(paymentService.createPayment(request, user));
    }

    @PutMapping("/payments/{id}/status")
    public ResponseEntity<Payment> updatePaymentStatus(@PathVariable Long id, @RequestBody Map<String, String> payload) {
        String status = payload.get("status");
        if (status == null || status.trim().isEmpty()) {
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity.ok(paymentService.updatePaymentStatus(id, status));
    }
}
