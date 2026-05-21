package com.rentifity.repository;

import com.rentifity.model.Car;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface CarRepository extends JpaRepository<Car, Long> {

    List<Car> findByStatus(String status);

    long countByStatus(String status);

    @Query("SELECT c FROM Car c WHERE (:status IS NULL OR c.status = :status) AND (:type IS NULL OR c.type = :type) AND (:search IS NULL OR c.name LIKE CONCAT('%', :search, '%') OR c.brand LIKE CONCAT('%', :search, '%'))")
    List<Car> findWithFilters(@Param("status") String status, @Param("type") String type, @Param("search") String search);
}
