package com.rentifity.dto.response;

import com.rentifity.model.Booking;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

public class ReportResponse {

    private long totalBookings;

    private BigDecimal totalRevenue;

    private long availableCars;

    private long totalCars;

    private List<Booking> recentBookings;

    private List<Map<String, Object>> revenueStats;

    public ReportResponse() {
    }

    public ReportResponse(long totalBookings, BigDecimal totalRevenue, long availableCars, long totalCars, List<Booking> recentBookings, List<Map<String, Object>> revenueStats) {
        this.totalBookings = totalBookings;
        this.totalRevenue = totalRevenue;
        this.availableCars = availableCars;
        this.totalCars = totalCars;
        this.recentBookings = recentBookings;
        this.revenueStats = revenueStats;
    }

    public long getTotalBookings() { return totalBookings; }
    public void setTotalBookings(long totalBookings) { this.totalBookings = totalBookings; }

    public BigDecimal getTotalRevenue() { return totalRevenue; }
    public void setTotalRevenue(BigDecimal totalRevenue) { this.totalRevenue = totalRevenue; }

    public long getAvailableCars() { return availableCars; }
    public void setAvailableCars(long availableCars) { this.availableCars = availableCars; }

    public long getTotalCars() { return totalCars; }
    public void setTotalCars(long totalCars) { this.totalCars = totalCars; }

    public List<Booking> getRecentBookings() { return recentBookings; }
    public void setRecentBookings(List<Booking> recentBookings) { this.recentBookings = recentBookings; }

    public List<Map<String, Object>> getRevenueStats() { return revenueStats; }
    public void setRevenueStats(List<Map<String, Object>> revenueStats) { this.revenueStats = revenueStats; }
}
