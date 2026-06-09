package com.rentifity.repository;
import com.rentifity.model.Review;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ReviewRepository extends JpaRepository<Review, Long> {
    List<Review> findByCarIdOrderByCreatedAtDesc(Long carId);
    boolean existsByBookingId(Long bookingId);
}
