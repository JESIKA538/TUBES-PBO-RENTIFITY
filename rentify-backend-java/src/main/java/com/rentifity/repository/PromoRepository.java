package com.rentifity.repository;
import com.rentifity.model.Promo;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface PromoRepository extends JpaRepository<Promo, Long> {
    Optional<Promo> findByCodeAndIsActiveTrue(String code);
}
