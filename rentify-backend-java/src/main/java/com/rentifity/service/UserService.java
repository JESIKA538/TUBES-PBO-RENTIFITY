package com.rentifity.service;

import com.rentifity.dto.request.UpdateProfileRequest;
import com.rentifity.exception.ResourceNotFoundException;
import com.rentifity.model.User;
import com.rentifity.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    public User getProfile(User user) {
        return user;
    }

    public void changePassword(User user, com.rentifity.dto.request.ChangePasswordRequest req) {
        User dbUser = userRepository.findById(user.getId())
                .orElseThrow(() -> new ResourceNotFoundException("User tidak ditemukan"));

        if (!passwordEncoder.matches(req.getOldPassword(), dbUser.getPassword())) {
            throw new RuntimeException("Kata sandi lama tidak cocok");
        }

        dbUser.setPassword(passwordEncoder.encode(req.getNewPassword()));
        userRepository.save(dbUser);
    }

    public User updateProfile(User user, UpdateProfileRequest req) {
        User dbUser = userRepository.findById(user.getId())
                .orElseThrow(() -> new ResourceNotFoundException("User tidak ditemukan"));

        if (req.getName() != null) dbUser.setName(req.getName());
        
        if (req.getEmail() != null && !req.getEmail().equals(dbUser.getEmail())) {
            if (userRepository.existsByEmail(req.getEmail())) {
                throw new RuntimeException("Email sudah terdaftar");
            }
            dbUser.setEmail(req.getEmail());
        }

        if (req.getPassword() != null && !req.getPassword().isBlank()) {
            dbUser.setPassword(passwordEncoder.encode(req.getPassword()));
        }
        if (req.getPhone() != null) dbUser.setPhone(req.getPhone());
        if (req.getOccupation() != null) dbUser.setOccupation(req.getOccupation());
        if (req.getAddress() != null) dbUser.setAddress(req.getAddress());
        if (req.getAvatar() != null) dbUser.setAvatar(req.getAvatar());

        return userRepository.save(dbUser);
    }

    public void deleteUser(Long id, User currentUser) {
        if (id.equals(currentUser.getId())) {
            throw new RuntimeException("Tidak dapat menghapus akun sendiri");
        }

        User user = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User tidak ditemukan"));

        userRepository.delete(user);
    }
}
