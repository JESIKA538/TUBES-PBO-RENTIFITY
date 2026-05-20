<?php

$baseUrl = 'http://127.0.0.1:8000/api';

function request($method, $path, $data = null, $token = null) {
    global $baseUrl;
    $url = $baseUrl . $path;
    
    $headers = [
        'Content-Type: application/json',
        'Accept: application/json'
    ];
    
    if ($token) {
        $headers[] = 'Authorization: Bearer ' . $token;
    }
    
    $options = [
        'http' => [
            'method' => $method,
            'header' => implode("\r\n", $headers),
            'ignore_errors' => true
        ]
    ];
    
    if ($data !== null) {
        $options['http']['content'] = json_encode($data);
    }
    
    $context = stream_context_create($options);
    $response = @file_get_contents($url, false, $context);
    
    $httpCode = 0;
    if (isset($http_response_header)) {
        preg_match('{HTTP\/\S*\s(\d+)}', $http_response_header[0], $match);
        $httpCode = intval($match[1]);
    }
    
    return [
        'status' => $httpCode,
        'body' => json_decode($response, true) ?? $response
    ];
}

function testLog($msg, $success = true) {
    if ($success) {
        echo "[+] \033[32mPASS\033[0m: $msg\n";
    } else {
        echo "[-] \033[31mFAIL\033[0m: $msg\n";
        exit(1);
    }
}

echo "=== MEMULAI PENGUJIAN API DINAMIS RENTIFY ===\n\n";

// 1. Uji Registrasi Customer Baru
$uniqueEmail = 'customer_test_' . time() . '@rentify.id';
$regData = [
    'name' => 'Test Customer',
    'email' => $uniqueEmail,
    'password' => 'password123',
    'phone' => '+628123456789',
    'occupation' => 'Software Engineer',
    'address' => 'Jl. Kebagusan No. 45, Jakarta Selatan'
];

$res = request('POST', '/register', $regData);
if ($res && $res['status'] === 201) {
    testLog("Registrasi customer baru berhasil (" . $uniqueEmail . ")");
    $custToken = $res['body']['access_token'];
    $custId = $res['body']['user']['id'];
} else {
    testLog("Registrasi customer baru gagal. Status: " . ($res ? $res['status'] : 'N/A') . ". Respon: " . json_encode($res ? $res['body'] : ''), false);
}

// 2. Uji Login Customer
$loginData = [
    'email' => $uniqueEmail,
    'password' => 'password123'
];
$res = request('POST', '/login', $loginData);
if ($res && $res['status'] === 200) {
    testLog("Login customer berhasil, token didapatkan.");
    $custToken = $res['body']['access_token'];
} else {
    testLog("Login customer gagal.", false);
}

// 3. Uji Cek Profile Customer
$res = request('GET', '/user', null, $custToken);
if ($res && $res['status'] === 200 && $res['body']['email'] === $uniqueEmail) {
    testLog("Mengambil data profil customer berhasil. Pekerjaan: " . $res['body']['occupation']);
} else {
    testLog("Mengambil profil customer gagal.", false);
}

// 4. Uji List Mobil
$res = request('GET', '/cars', null, $custToken);
if ($res && $res['status'] === 200 && count($res['body']) > 0) {
    $car = $res['body'][0];
    testLog("Daftar mobil berhasil diambil. Menemukan " . count($res['body']) . " mobil. Memilih: " . $car['name']);
    $carId = $car['id'];
    $pricePerDay = $car['price_per_day'];
} else {
    testLog("Daftar mobil kosong atau gagal diambil.", false);
}

// 5. Uji Detail Mobil
$res = request('GET', '/cars/' . $carId, null, $custToken);
if ($res && $res['status'] === 200 && $res['body']['name'] === $car['name']) {
    testLog("Mengambil detail mobil '" . $car['name'] . "' berhasil.");
} else {
    testLog("Mengambil detail mobil gagal.", false);
}

// 6. Uji Pemesanan (Booking) Mobil
$today = date('Y-m-d');
$tomorrow = date('Y-m-d', strtotime('+3 days'));
$bookingData = [
    'car_id' => $carId,
    'start_date' => $today,
    'end_date' => $tomorrow,
    'notes' => 'Tolong mobil dibersihkan terlebih dahulu.'
];

$res = request('POST', '/bookings', $bookingData, $custToken);
if ($res && $res['status'] === 201) {
    $booking = $res['body']['booking'];
    testLog("Membuat booking baru berhasil. Booking ID: " . $booking['id'] . ", Total Harga: Rp " . number_format($booking['total_price'], 0, ',', '.'));
    $bookingId = $booking['id'];
    $totalPrice = $booking['total_price'];
} else {
    testLog("Membuat booking baru gagal. Respon: " . json_encode($res), false);
}

// 7. Uji Booking Mobil Yang Sama (Harus Gagal karena status mobil sudah Rented)
$res = request('POST', '/bookings', $bookingData, $custToken);
if ($res && $res['status'] === 422) {
    testLog("Validasi ketersediaan mobil bekerja. Pemesanan ganda ditolak dengan benar (422).");
} else {
    testLog("Pemesanan mobil yang sedang disewa seharusnya gagal tetapi berhasil atau menghasilkan status berbeda.", false);
}

// 8. Uji Pembayaran (Payment)
$paymentData = [
    'booking_id' => $bookingId,
    'payment_method' => 'Transfer Bank BCA',
    'amount' => $totalPrice,
    'proof_of_payment' => 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=' // 1x1 pixel base64 dummy
];

$res = request('POST', '/payments', $paymentData, $custToken);
if ($res && $res['status'] === 201) {
    testLog("Unggah pembayaran & konfirmasi booking otomatis berhasil.");
} else {
    testLog("Unggah pembayaran gagal. Respon: " . json_encode($res), false);
}

// 9. Uji Login Admin
$adminLoginData = [
    'email' => 'rahmaarifinjesikametania@gmail.com',
    'password' => 'Jesica123@'
];
$res = request('POST', '/login', $adminLoginData);
if ($res && $res['status'] === 200) {
    testLog("Login admin (Jesica Rahma Arifin) berhasil.");
    $adminToken = $res['body']['access_token'];
} else {
    testLog("Login admin gagal.", false);
}

// 10. Uji Dashboard Admin / Laporan (/reports)
$res = request('GET', '/reports', null, $adminToken);
if ($res && $res['status'] === 200) {
    $stats = $res['body'];
    testLog("Mengambil laporan admin berhasil. Total Pendapatan: Rp " . number_format($stats['total_revenue'], 0, ',', '.'));
    testLog("Laporan - Jumlah Mobil: " . $stats['total_cars'] . ", Transaksi Terbaru: " . count($stats['recent_bookings']));
} else {
    testLog("Mengambil laporan admin gagal.", false);
}

// 11. Uji CRUD Mobil oleh Admin
// 11a. Create Car
$newCarData = [
    'name' => 'Tesla Cybertruck',
    'brand' => 'Tesla',
    'type' => 'SUV / Truck',
    'transmission' => 'Otomatis',
    'fuel_type' => 'Listrik',
    'price_per_day' => 1500000,
    'status' => 'available',
    'description' => 'Truk listrik masa depan anti peluru.'
];
$res = request('POST', '/cars', $newCarData, $adminToken);
if ($res && $res['status'] === 201) {
    $newCarId = $res['body']['car']['id'];
    testLog("Admin: Berhasil menambahkan armada baru: " . $res['body']['car']['name']);
} else {
    testLog("Admin: Gagal menambahkan armada baru.", false);
}

// 11b. Update Car
$updateCarData = [
    'price_per_day' => 1750000,
    'status' => 'maintenance'
];
$res = request('PUT', '/cars/' . $newCarId, $updateCarData, $adminToken);
if ($res && $res['status'] === 200 && $res['body']['car']['status'] === 'maintenance') {
    testLog("Admin: Berhasil memperbarui harga & status armada baru menjadi maintenance.");
} else {
    testLog("Admin: Gagal memperbarui armada.", false);
}

// 11c. Delete Car
$res = request('DELETE', '/cars/' . $newCarId, null, $adminToken);
if ($res && $res['status'] === 200) {
    testLog("Admin: Berhasil menghapus armada.");
} else {
    testLog("Admin: Gagal menghapus armada.", false);
}

// 12. Uji Proteksi Manajemen Pengguna
// 12a. Ambil Semua User
$res = request('GET', '/users', null, $adminToken);
if ($res && $res['status'] === 200) {
    testLog("Admin: Berhasil mengambil seluruh daftar pengguna (" . count($res['body']) . " terdaftar).");
} else {
    testLog("Admin: Gagal mengambil daftar pengguna.", false);
}

// 12b. Hapus Akun Sendiri (Harus Ditolak)
$adminId = 1; // Alex Walker is user id 1
$res = request('DELETE', '/users/' . $adminId, null, $adminToken);
if ($res && $res['status'] === 400) {
    testLog("Admin: Proteksi penghapusan diri sendiri berhasil dibuktikan (Ditolak dengan 400).");
} else {
    testLog("Admin: Menghapus akun sendiri tidak ditolak!", false);
}

// 12c. Hapus Akun Test Customer (Harus Berhasil)
$res = request('DELETE', '/users/' . $custId, null, $adminToken);
if ($res && $res['status'] === 200) {
    testLog("Admin: Berhasil menghapus akun pengguna uji coba (Test Customer).");
} else {
    testLog("Admin: Gagal menghapus akun pengguna uji coba.", false);
}

echo "\n\033[32m=========================================================\033[0m\n";
echo "\033[32m[OK] SEMUA PENGUJIAN INTEGRASI BERHASIL DISAJIKAN 100%! [OK]\033[0m\n";
echo "\033[32m=========================================================\033[0m\n";
