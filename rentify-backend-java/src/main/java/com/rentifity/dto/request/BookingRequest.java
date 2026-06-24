package com.rentifity.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public Booking requestReturn(Long bookingId, User user) {

    // Mencari data booking berdasarkan ID booking
    // Jika tidak ditemukan akan muncul error "Booking tidak ditemukan"
    Booking booking = bookingRepository.findById(bookingId)
            .orElseThrow(() -> new ResourceNotFoundException("Booking tidak ditemukan"));

    // Validasi hak akses
    // Hanya pemilik booking atau admin yang boleh melakukan pengembalian
    if (!booking.getUser().getId().equals(user.getId()) && !user.getRole().equals("admin")) {
        throw new RuntimeException("Unauthorized");
    }

    // Validasi status booking
    // Pengembalian hanya bisa dilakukan jika status booking sudah confirmed
    if (!"confirmed".equals(booking.getStatus())) {
        throw new RuntimeException("Hanya pesanan aktif (dikonfirmasi) yang dapat dikembalikan");
    }

    // Mengambil tanggal hari ini menggunakan zona waktu Indonesia
    LocalDate today = LocalDate.now(ZoneId.of("Asia/Jakarta"));

    // Mengecek apakah pengembalian melebihi tanggal akhir sewa
    if (today.isAfter(booking.getEndDate())) {

        // Menghitung jumlah hari keterlambatan
        long daysLate = ChronoUnit.DAYS.between(
                booking.getEndDate(),
                today
        );

        // Menghitung denda keterlambatan
        // Rumus:
        // total harga rental × 10% × jumlah hari terlambat
        BigDecimal penalty = booking.getTotalPrice()
                .multiply(BigDecimal.valueOf(0.1))
                .multiply(BigDecimal.valueOf(daysLate));

        // Menyimpan nilai denda ke atribut lateFee
        booking.setLateFee(penalty);

    } else {

        // Jika tidak terlambat maka denda = 0
        booking.setLateFee(BigDecimal.ZERO);
    }

    // Status diubah menjadi returning
    // Artinya user sudah mengajukan pengembalian
    // dan sedang menunggu verifikasi admin
    booking.setStatus("returning");

    // Menyimpan perubahan ke database
    Booking savedBooking = bookingRepository.save(booking);

    // Mengirim notifikasi kepada admin
    notificationService.createNotificationForRole(
            "admin",
            "Pengguna " + user.getName()
                    + " telah meminta pengembalian mobil untuk pesanan #RT-"
                    + savedBooking.getId()
    );

    return savedBooking;
}
