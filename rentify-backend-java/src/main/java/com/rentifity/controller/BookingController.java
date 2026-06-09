package com.rentifity.controller;

import com.rentifity.dto.request.BookingRequest;
import com.rentifity.dto.response.ReportResponse;
import com.rentifity.model.Booking;
import com.rentifity.model.User;
import com.rentifity.security.CustomUserDetailsService;
import com.rentifity.service.BookingService;
import com.rentifity.service.NotificationService;
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
public class BookingController {

    @Autowired
    private BookingService bookingService;

    @Autowired
    private CustomUserDetailsService customUserDetailsService;

    @Autowired
    private NotificationService notificationService;

    private User getCurrentUser(Authentication authentication) {
        return customUserDetailsService.getUserByEmail(authentication.getName());
    }

    @GetMapping("/bookings")
    public ResponseEntity<List<Booking>> index(Authentication auth) {
        User user = getCurrentUser(auth);
        return ResponseEntity.ok(bookingService.getAllBookings(user));
    }

    @PostMapping("/bookings")
    public ResponseEntity<Map<String, Object>> store(@Valid @RequestBody BookingRequest request, Authentication auth) {
        User user = getCurrentUser(auth);
        Booking booking = bookingService.createBooking(request, user);
        return ResponseEntity.status(HttpStatus.CREATED).body(Map.of("message", "Booking created successfully", "booking", booking));
    }

    @GetMapping("/reports")
    public ResponseEntity<ReportResponse> reports() {
        return ResponseEntity.ok(bookingService.getReports());
    }

    @PutMapping("/bookings/{id}/return")
    public ResponseEntity<Map<String, Object>> requestReturn(@PathVariable Long id, Authentication auth) {
        User user = getCurrentUser(auth);
        Booking booking = bookingService.requestReturn(id, user);
        return ResponseEntity.ok(Map.of("message", "Pengajuan pengembalian berhasil", "booking", booking));
    }

    @PutMapping("/bookings/{id}/confirm-return")
    public ResponseEntity<Map<String, Object>> confirmReturn(@PathVariable Long id, Authentication auth) {
        User user = getCurrentUser(auth);
        if (!"admin".equals(user.getRole())) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).body(Map.of("message", "Akses ditolak"));
        }
        Booking booking = bookingService.confirmReturn(id);
        return ResponseEntity.ok(Map.of("message", "Pengembalian mobil berhasil dikonfirmasi", "booking", booking));
    }
}
