package com.rentifity.dto.response;

import com.rentifity.model.Booking;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ReportResponse {

    private long totalBookings;

    private BigDecimal totalRevenue;

    private long availableCars;

    private long totalCars;

    private List<Booking> recentBookings;

    private List<Map<String, Object>> revenueStats;
}
