package com.rentifity.model;
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
