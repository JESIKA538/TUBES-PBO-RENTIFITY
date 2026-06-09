package com.rentifity.service;

import com.rentifity.model.Notification;
import com.rentifity.model.User;
import com.rentifity.repository.NotificationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class NotificationService {

    @Autowired
    private NotificationRepository notificationRepository;

    public Notification createNotificationForUser(User user, String message) {
        Notification notification = new Notification(user, user.getRole(), message);
        return notificationRepository.save(notification);
    }

    public Notification createNotificationForRole(String role, String message) {
        Notification notification = new Notification(null, role, message);
        return notificationRepository.save(notification);
    }

    public List<Notification> getUserNotifications(User user) {
        return notificationRepository.findRelevantNotifications(user.getId(), user.getRole());
    }

    public void markAsRead(Long id) {
        Notification notification = notificationRepository.findById(id).orElse(null);
        if (notification != null) {
            notification.setRead(true);
            notificationRepository.save(notification);
        }
    }
}
