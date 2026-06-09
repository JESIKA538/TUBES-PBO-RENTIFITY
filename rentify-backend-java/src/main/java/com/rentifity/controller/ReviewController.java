package com.rentifity.controller;
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
