package com.rentifity.repository;

import com.rentifity.model.Notification;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface NotificationRepository extends JpaRepository<Notification, Long> {
    
    // Fetch notifications for a specific user OR for their role globally
    @Query("SELECT n FROM Notification n WHERE n.user.id = :userId OR (n.user IS NULL AND n.targetRole = :role) ORDER BY n.createdAt DESC")
    List<Notification> findRelevantNotifications(Long userId, String role);
}
