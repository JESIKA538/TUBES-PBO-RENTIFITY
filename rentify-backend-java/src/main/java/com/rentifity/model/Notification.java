package com.rentifity.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "notifications")
public class Notification {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Optional: if null, it could mean it's broadcasted, but let's keep it simple.
    // Admin notifications can be tied to specific admin users or a general 'target_role'.
    // To simplify, we will just map a receiver user_id. If we want all admins to get it, 
    // we can create a notification for each admin, or add a 'targetRole' column.
    // Let's add targetRole to make global admin notifications easy without looping.
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = true, foreignKey = @ForeignKey(value = ConstraintMode.NO_CONSTRAINT))
    private User user; // Specific user receiver. If null, use targetRole.

    @Column(name = "target_role")
    private String targetRole; // e.g., 'ADMIN', 'USER' (if user is null, all users of this role receive it)

    @Column(columnDefinition = "TEXT", nullable = false)
    private String message;

    @Column(name = "is_read", nullable = false)
    private boolean isRead = false;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }

    public Notification() {}

    public Notification(User user, String targetRole, String message) {
        this.user = user;
        this.targetRole = targetRole;
        this.message = message;
        this.isRead = false;
    }

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }

    public String getTargetRole() { return targetRole; }
    public void setTargetRole(String targetRole) { this.targetRole = targetRole; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public boolean isRead() { return isRead; }
    public void setRead(boolean read) { isRead = read; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
