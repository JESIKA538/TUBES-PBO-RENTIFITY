import os

BASE_DIR = r"c:\TUBES PBO RENTIFITY\rentify-backend-java\src\main\java\com\rentifity"

# 1. Models
PROMO_MODEL = """package com.rentifity.model;
import jakarta.persistence.*;
import java.math.BigDecimal;

@Entity
@Table(name = "promos")
public class Promo {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(unique = true, nullable = false)
    private String code;
    
    @Column(name = "discount_percentage", nullable = false)
    private BigDecimal discountPercentage;
    
    @Column(name = "max_discount")
    private BigDecimal maxDiscount;
    
    @Column(name = "is_active")
    private boolean isActive = true;

    public Promo() {}
    public Promo(String code, BigDecimal discountPercentage, BigDecimal maxDiscount) {
        this.code = code;
        this.discountPercentage = discountPercentage;
        this.maxDiscount = maxDiscount;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getCode() { return code; }
    public void setCode(String code) { this.code = code; }
    public BigDecimal getDiscountPercentage() { return discountPercentage; }
    public void setDiscountPercentage(BigDecimal discountPercentage) { this.discountPercentage = discountPercentage; }
    public BigDecimal getMaxDiscount() { return maxDiscount; }
    public void setMaxDiscount(BigDecimal maxDiscount) { this.maxDiscount = maxDiscount; }
    public boolean isActive() { return isActive; }
    public void setActive(boolean active) { isActive = active; }
}
"""

REVIEW_MODEL = """package com.rentifity.model;
import jakarta.persistence.*;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.time.LocalDateTime;

@Entity
@Table(name = "reviews")
public class Review {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "booking_id", nullable = false)
    @JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
    private Booking booking;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "car_id", nullable = false)
    @JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
    private Car car;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    @JsonIgnoreProperties({"hibernateLazyInitializer", "handler", "password"})
    private User user;
    
    @Column(nullable = false)
    private int rating;
    
    @Column(columnDefinition = "TEXT")
    private String comment;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @PrePersist
    protected void onCreate() { this.createdAt = LocalDateTime.now(); }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Booking getBooking() { return booking; }
    public void setBooking(Booking booking) { this.booking = booking; }
    public Car getCar() { return car; }
    public void setCar(Car car) { this.car = car; }
    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }
    public int getRating() { return rating; }
    public void setRating(int rating) { this.rating = rating; }
    public String getComment() { return comment; }
    public void setComment(String comment) { this.comment = comment; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
"""

# 2. Repositories
PROMO_REPO = """package com.rentifity.repository;
import com.rentifity.model.Promo;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface PromoRepository extends JpaRepository<Promo, Long> {
    Optional<Promo> findByCodeAndIsActiveTrue(String code);
}
"""

REVIEW_REPO = """package com.rentifity.repository;
import com.rentifity.model.Review;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ReviewRepository extends JpaRepository<Review, Long> {
    List<Review> findByCarIdOrderByCreatedAtDesc(Long carId);
    boolean existsByBookingId(Long bookingId);
}
"""

# 3. DTOs
REVIEW_REQ = """package com.rentifity.dto.request;
public class ReviewRequest {
    private Long bookingId;
    private int rating;
    private String comment;
    public Long getBookingId() { return bookingId; }
    public void setBookingId(Long bookingId) { this.bookingId = bookingId; }
    public int getRating() { return rating; }
    public void setRating(int rating) { this.rating = rating; }
    public String getComment() { return comment; }
    public void setComment(String comment) { this.comment = comment; }
}
"""

# 4. Controllers
REVIEW_CTRL = """package com.rentifity.controller;
import com.rentifity.dto.request.ReviewRequest;
import com.rentifity.model.Review;
import com.rentifity.model.User;
import com.rentifity.security.CustomUserDetailsService;
import com.rentifity.service.ReviewService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api")
public class ReviewController {
    @Autowired
    private ReviewService reviewService;
    
    @Autowired
    private CustomUserDetailsService customUserDetailsService;
    
    @PostMapping("/reviews")
    public ResponseEntity<Review> createReview(@RequestBody ReviewRequest req, Authentication auth) {
        User user = customUserDetailsService.getUserByEmail(auth.getName());
        return ResponseEntity.ok(reviewService.createReview(req, user));
    }
    
    @GetMapping("/cars/{id}/reviews")
    public ResponseEntity<List<Review>> getCarReviews(@PathVariable Long id) {
        return ResponseEntity.ok(reviewService.getCarReviews(id));
    }
}
"""

PROMO_CTRL = """package com.rentifity.controller;
import com.rentifity.model.Promo;
import com.rentifity.repository.PromoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/promos")
public class PromoController {
    @Autowired
    private PromoRepository promoRepository;
    
    @GetMapping("/validate")
    public ResponseEntity<?> validatePromo(@RequestParam String code) {
        Optional<Promo> promo = promoRepository.findByCodeAndIsActiveTrue(code);
        if (promo.isPresent()) {
            return ResponseEntity.ok(promo.get());
        }
        return ResponseEntity.badRequest().body(Map.of("message", "Kode promo tidak valid atau sudah kadaluarsa"));
    }
}
"""

# 5. Review Service
REVIEW_SVC = """package com.rentifity.service;
import com.rentifity.dto.request.ReviewRequest;
import com.rentifity.exception.ResourceNotFoundException;
import com.rentifity.model.Booking;
import com.rentifity.model.Review;
import com.rentifity.model.User;
import com.rentifity.repository.BookingRepository;
import com.rentifity.repository.ReviewRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class ReviewService {
    @Autowired
    private ReviewRepository reviewRepository;
    
    @Autowired
    private BookingRepository bookingRepository;
    
    public Review createReview(ReviewRequest req, User user) {
        Booking booking = bookingRepository.findById(req.getBookingId())
                .orElseThrow(() -> new ResourceNotFoundException("Booking tidak ditemukan"));
                
        if (!booking.getUser().getId().equals(user.getId())) {
            throw new RuntimeException("Unauthorized");
        }
        
        if (!"completed".equals(booking.getStatus())) {
            throw new RuntimeException("Pesanan belum selesai");
        }
        
        if (reviewRepository.existsByBookingId(booking.getId())) {
            throw new RuntimeException("Ulasan sudah pernah diberikan");
        }
        
        Review review = new Review();
        review.setBooking(booking);
        review.setCar(booking.getCar());
        review.setUser(user);
        review.setRating(req.getRating());
        review.setComment(req.getComment());
        
        return reviewRepository.save(review);
    }
    
    public List<Review> getCarReviews(Long carId) {
        return reviewRepository.findByCarIdOrderByCreatedAtDesc(carId);
    }
}
"""

files_to_write = {
    "model/Promo.java": PROMO_MODEL,
    "model/Review.java": REVIEW_MODEL,
    "repository/PromoRepository.java": PROMO_REPO,
    "repository/ReviewRepository.java": REVIEW_REPO,
    "dto/request/ReviewRequest.java": REVIEW_REQ,
    "controller/ReviewController.java": REVIEW_CTRL,
    "controller/PromoController.java": PROMO_CTRL,
    "service/ReviewService.java": REVIEW_SVC
}

for path, content in files_to_write.items():
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)

print("Files generated successfully.")
