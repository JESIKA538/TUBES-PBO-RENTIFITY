import os

BASE_DIR = r"c:\TUBES PBO RENTIFITY\rentify-backend-java\src\main\java\com\rentifity"

# Update Booking.java
booking_path = os.path.join(BASE_DIR, "model/Booking.java")
with open(booking_path, "r") as f:
    booking_code = f.read()

# Add fields to Booking if not present
if "deliveryOption" not in booking_code:
    fields_to_add = """
    @Column(name = "delivery_option")
    private String deliveryOption; // e.g., 'pickup', 'delivery'

    @Column(name = "delivery_address", columnDefinition = "TEXT")
    private String deliveryAddress;

    @Column(name = "late_fee")
    private BigDecimal lateFee;
    
    public String getDeliveryOption() { return deliveryOption; }
    public void setDeliveryOption(String deliveryOption) { this.deliveryOption = deliveryOption; }
    public String getDeliveryAddress() { return deliveryAddress; }
    public void setDeliveryAddress(String deliveryAddress) { this.deliveryAddress = deliveryAddress; }
    public BigDecimal getLateFee() { return lateFee; }
    public void setLateFee(BigDecimal lateFee) { this.lateFee = lateFee; }
"""
    # Insert before last closing brace
    booking_code = booking_code[:booking_code.rfind("}")] + fields_to_add + "\n}\n"
    with open(booking_path, "w") as f:
        f.write(booking_code)

# Update BookingRequest.java
req_path = os.path.join(BASE_DIR, "dto/request/BookingRequest.java")
with open(req_path, "r") as f:
    req_code = f.read()

if "deliveryOption" not in req_code:
    fields_to_add = """
    private String deliveryOption;
    private String deliveryAddress;
    public String getDeliveryOption() { return deliveryOption; }
    public void setDeliveryOption(String deliveryOption) { this.deliveryOption = deliveryOption; }
    public String getDeliveryAddress() { return deliveryAddress; }
    public void setDeliveryAddress(String deliveryAddress) { this.deliveryAddress = deliveryAddress; }
"""
    req_code = req_code[:req_code.rfind("}")] + fields_to_add + "\n}\n"
    with open(req_path, "w") as f:
        f.write(req_code)

# Update BookingService.java
svc_path = os.path.join(BASE_DIR, "service/BookingService.java")
with open(svc_path, "r") as f:
    svc_code = f.read()

if "deliveryOption" not in svc_code:
    svc_code = svc_code.replace(
        ".notes(req.getNotes())",
        ".notes(req.getNotes())\n                .deliveryOption(req.getDeliveryOption())\n                .deliveryAddress(req.getDeliveryAddress())\n                .lateFee(BigDecimal.ZERO)"
    )
    
    # Add late fee logic in requestReturn
    late_logic = """
        // Calculate late fee if returned after endDate
        LocalDate today = LocalDate.now(ZoneId.of("Asia/Jakarta"));
        if (today.isAfter(booking.getEndDate())) {
            long daysLate = java.time.temporal.ChronoUnit.DAYS.between(booking.getEndDate(), today);
            // Example: 10% of total price per day late
            BigDecimal penalty = booking.getTotalPrice().multiply(BigDecimal.valueOf(0.1)).multiply(BigDecimal.valueOf(daysLate));
            booking.setLateFee(penalty);
        } else {
            booking.setLateFee(BigDecimal.ZERO);
        }
        booking.setStatus("returning");"""
    
    svc_code = svc_code.replace('booking.setStatus("returning");', late_logic)
    with open(svc_path, "w") as f:
        f.write(svc_code)

# Update CarRepository.java for advanced search
car_repo_path = os.path.join(BASE_DIR, "repository/CarRepository.java")
with open(car_repo_path, "r") as f:
    car_repo_code = f.read()

if "findByFilters" not in car_repo_code:
    custom_query = """
    @org.springframework.data.jpa.repository.Query("SELECT c FROM Car c WHERE " +
           "(:minPrice IS NULL OR c.pricePerDay >= :minPrice) AND " +
           "(:maxPrice IS NULL OR c.pricePerDay <= :maxPrice) AND " +
           "(:transmission IS NULL OR :transmission = '' OR c.transmission = :transmission) AND " +
           "(:fuelType IS NULL OR :fuelType = '' OR c.fuelType = :fuelType)")
    java.util.List<com.rentifity.model.Car> findByFilters(
        @org.springframework.data.repository.query.Param("minPrice") java.math.BigDecimal minPrice,
        @org.springframework.data.repository.query.Param("maxPrice") java.math.BigDecimal maxPrice,
        @org.springframework.data.repository.query.Param("transmission") String transmission,
        @org.springframework.data.repository.query.Param("fuelType") String fuelType
    );
"""
    car_repo_code = car_repo_code[:car_repo_code.rfind("}")] + custom_query + "\n}\n"
    with open(car_repo_path, "w") as f:
        f.write(car_repo_code)

# Update CarController.java
car_ctrl_path = os.path.join(BASE_DIR, "controller/CarController.java")
with open(car_ctrl_path, "r") as f:
    car_ctrl_code = f.read()

if "minPrice" not in car_ctrl_code:
    # Replace public ResponseEntity<List<Car>> index() with the new one
    old_index = """    @GetMapping("/cars")
    public ResponseEntity<List<Car>> index() {
        return ResponseEntity.ok(carRepository.findAll());
    }"""
    
    new_index = """    @GetMapping("/cars")
    public ResponseEntity<java.util.List<Car>> index(
            @RequestParam(required = false) java.math.BigDecimal minPrice,
            @RequestParam(required = false) java.math.BigDecimal maxPrice,
            @RequestParam(required = false) String transmission,
            @RequestParam(required = false) String fuelType) {
        
        if (minPrice != null || maxPrice != null || (transmission != null && !transmission.isEmpty()) || (fuelType != null && !fuelType.isEmpty())) {
            return ResponseEntity.ok(carRepository.findByFilters(minPrice, maxPrice, transmission, fuelType));
        }
        return ResponseEntity.ok(carRepository.findAll());
    }"""
    
    car_ctrl_code = car_ctrl_code.replace(old_index, new_index)
    with open(car_ctrl_path, "w") as f:
        f.write(car_ctrl_code)

print("Backend integrations complete.")
