package com.rentifity.repository;
// jpa membantu menghubungkan java dengan DBMYSQL
// jadi kita tidak perlu menulis query manual
// jpa repository menyediakan method bawaan seperti save, delete, dll
import com.rentifity.model.Booking;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.math.BigDecimal;
import java.util.List;

public interface BookingRepository extends JpaRepository<Booking, Long> {

    List<Booking> findByUserIdOrderByCreatedAtDesc(Long userId);

    List<Booking> findAllByOrderByCreatedAtDesc();

    List<Booking> findTop5ByOrderByCreatedAtDesc();

    @Query("SELECT COALESCE(SUM(b.totalPrice), 0) FROM Booking b WHERE b.status IN ('confirmed', 'completed')")
    BigDecimal getTotalRevenue();

    @Query("SELECT COALESCE(SUM(b.totalPrice), 0) FROM Booking b WHERE b.status IN ('confirmed', 'completed') AND YEAR(b.startDate) = :year AND MONTH(b.startDate) = :month")
    BigDecimal getRevenueByMonth(int year, int month);
}
