package com.rentifity.controller;

import com.rentifity.dto.request.UpdateProfileRequest;
import com.rentifity.model.User;
import com.rentifity.security.CustomUserDetailsService;
import com.rentifity.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class UserController {

    @Autowired
    private UserService userService;

    @Autowired
    private CustomUserDetailsService customUserDetailsService;

    private User getCurrentUser(Authentication authentication) {
        return customUserDetailsService.getUserByEmail(authentication.getName());
    }

    @GetMapping("/user")
    public ResponseEntity<User> show(Authentication auth) {
        User user = getCurrentUser(auth);
        return ResponseEntity.ok(userService.getProfile(user));
    }

    @PutMapping("/users/profile")
    public ResponseEntity<User> updateProfile(@Valid @RequestBody com.rentifity.dto.request.UpdateProfileRequest request, Authentication auth) {
        User user = getCurrentUser(auth);
        return ResponseEntity.ok(userService.updateProfile(user, request));
    }

    @PutMapping("/users/password")
    public ResponseEntity<Map<String, String>> changePassword(@Valid @RequestBody com.rentifity.dto.request.ChangePasswordRequest request, Authentication auth) {
        User user = getCurrentUser(auth);
        userService.changePassword(user, request);
        return ResponseEntity.ok(Map.of("message", "Kata sandi berhasil diubah"));
    }

    @GetMapping("/users")
    public ResponseEntity<List<User>> index(Authentication auth) {
        User user = getCurrentUser(auth);
        if (!user.getRole().equals("admin")) {
            throw new RuntimeException("Forbidden");
        }
        return ResponseEntity.ok(userService.getAllUsers());
    }

    @DeleteMapping("/users/{id}")
    public ResponseEntity<Map<String, String>> destroy(@PathVariable Long id, Authentication auth) {
        User user = getCurrentUser(auth);
        if (!user.getRole().equals("admin")) {
            throw new RuntimeException("Forbidden");
        }
        userService.deleteUser(id, user);
        return ResponseEntity.ok(Map.of("message", "User berhasil dihapus"));
    }
}
