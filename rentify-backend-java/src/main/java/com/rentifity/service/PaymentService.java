package com.rentifity.service;

import com.rentifity.dto.request.PaymentRequest;
import com.rentifity.exception.ResourceNotFoundException;
import com.rentifity.model.Booking;
import com.rentifity.model.Car;
import com.rentifity.model.Payment;
import com.rentifity.model.User;
import com.rentifity.repository.BookingRepository;
import com.rentifity.repository.CarRepository;
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

    @Autowired
    private CarRepository carRepository;

    @Autowired
    private NotificationService notificationService;

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

        String billingCode = "";
        if ("Transfer Bank".equalsIgnoreCase(req.getPaymentMethod())) {
            // Generate 16 digit VA
            billingCode = String.format("%04d%04d%04d%04d", 
                (int)(Math.random() * 10000), (int)(Math.random() * 10000), 
                (int)(Math.random() * 10000), (int)(Math.random() * 10000));
        } else if ("E-Wallet".equalsIgnoreCase(req.getPaymentMethod())) {
            // Generate E-Wallet Ref
            String prefix = req.getPaymentChannel() != null ? req.getPaymentChannel().toUpperCase() : "PAY";
            billingCode = prefix + "-" + (long)(Math.random() * 10000000000L);
        }

        Payment payment = Payment.builder()
                .booking(booking)
                .paymentMethod(req.getPaymentMethod())
                .paymentChannel(req.getPaymentChannel())
                .billingCode(billingCode)
                .amount(req.getAmount())
                .status("pending")
                .proofOfPayment(req.getProofOfPayment())
                .build();

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
                notificationService.createNotificationForRole("admin", "Pembayaran untuk pesanan #RT-" + payment.getBooking().getId() + " telah berhasil. Mobil siap disewakan.");
                notificationService.createNotificationForUser(payment.getBooking().getUser(), "Pembayaran Anda untuk pesanan #RT-" + payment.getBooking().getId() + " berhasil! Mobil " + payment.getBooking().getCar().getName() + " siap diambil.");
            }
        } else if ("failed".equalsIgnoreCase(status) || "rejected".equalsIgnoreCase(status)) {
            if (payment.getBooking() != null) {
                Booking booking = payment.getBooking();
                booking.setStatus("cancelled");
                if (booking.getCar() != null) {
                    Car car = booking.getCar();
                    car.setStatus("available");
                    carRepository.save(car);
                }
                notificationService.createNotificationForUser(booking.getUser(), "Maaf, pembayaran untuk pesanan #RT-" + booking.getId() + " gagal atau ditolak. Pesanan dibatalkan.");
            }
        }
        
        return paymentRepository.save(payment);
    }
}
