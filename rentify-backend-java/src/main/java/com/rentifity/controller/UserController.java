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
import java.util.HashMap;

@RestController
@RequestMapping("/api")
public class UserController {

    @Autowired
    private UserService userService;

    @Autowired
    private CustomUserDetailsService customUserDetailsService;

    @Autowired
    private com.rentifity.security.JwtUtil jwtUtil;

    private User getCurrentUser(Authentication authentication) {
        return customUserDetailsService.getUserByEmail(authentication.getName());
    }

    @GetMapping("/user")
    public ResponseEntity<User> show(Authentication auth) {
        User user = getCurrentUser(auth);
        return ResponseEntity.ok(userService.getProfile(user));
    }

    @PutMapping("/users/profile")
    public ResponseEntity<Map<String, Object>> updateProfile(@Valid @RequestBody com.rentifity.dto.request.UpdateProfileRequest request, Authentication auth) {
        User user = getCurrentUser(auth);
        String oldEmail = user.getEmail();

        User updatedUser = userService.updateProfile(user, request);

        Map<String, Object> response = new HashMap<>();
        response.put("message", "Profil berhasil diperbarui");
        response.put("user", updatedUser);

        if (!updatedUser.getEmail().equals(oldEmail)) {
            String newToken = jwtUtil.generateToken(updatedUser.getEmail());
            response.put("token", newToken);
        }

        return ResponseEntity.ok(response);
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
        return ResponseEntity.ok(userService.getAllUsers());
    }

    @DeleteMapping("/users/{id}")
    public ResponseEntity<Map<String, String>> destroy(@PathVariable Long id, Authentication auth) {
        User user = getCurrentUser(auth);
        userService.deleteUser(id, user);
        return ResponseEntity.ok(Map.of("message", "User berhasil dihapus"));
    }
}
