package com.rentifity.service;

import com.rentifity.dto.request.PaymentRequest;
import com.rentifity.exception.ResourceNotFoundException;
import com.rentifity.model.Booking;
import com.rentifity.model.Payment;
import com.rentifity.model.User;
import com.rentifity.repository.BookingRepository;
import com.rentifity.repository.PaymentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PaymentService {

    @Autowired
    private PaymentRepository paymentRepository;

    @Autowired
    private BookingRepository bookingRepository;

    public List<Payment> getAllPayments(User user) {
        if (user.getRole().equals("admin")) {
            return paymentRepository.findAllByOrderByCreatedAtDesc();
        }
        return paymentRepository.findByUserId(user.getId());
    }

    public Payment createPayment(PaymentRequest req, User user) {
        Booking booking = bookingRepository.findById(req.getBookingId())
                .orElseThrow(() -> new ResourceNotFoundException("Booking tidak ditemukan"));

        if (!booking.getUser().getId().equals(user.getId()) && !user.getRole().equals("admin")) {
            throw new RuntimeException("Unauthorized");
        }

        Payment payment = Payment.builder()
                .booking(booking)
                .paymentMethod(req.getPaymentMethod())
                .amount(req.getAmount())
                .status("approved")
                .proofOfPayment(req.getProofOfPayment())
                .build();

        booking.setStatus("confirmed");
        bookingRepository.save(booking);

        return paymentRepository.save(payment);
    }

    public Payment updatePaymentStatus(Long paymentId, String status) {
        Payment payment = paymentRepository.findById(paymentId)
                .orElseThrow(() -> new ResourceNotFoundException("Payment tidak ditemukan dengan id: " + paymentId));
        payment.setStatus(status);
        
        // If payment is approved, update booking status to confirmed if it was pending
        if ("approved".equalsIgnoreCase(status) || "success".equalsIgnoreCase(status)) {
            if (payment.getBooking() != null && "pending".equalsIgnoreCase(payment.getBooking().getStatus())) {
                payment.getBooking().setStatus("confirmed");
            }
        } else if ("failed".equalsIgnoreCase(status) || "rejected".equalsIgnoreCase(status)) {
            if (payment.getBooking() != null) {
                payment.getBooking().setStatus("cancelled");
            }
        }
        
        return paymentRepository.save(payment);
    }
}
