package com.rentifity.service;
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
