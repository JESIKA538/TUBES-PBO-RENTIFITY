<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    use WithoutModelEvents;

    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        // 1. Seed Users
        User::create([
            'name' => 'Jesica Rahma Arifin',
            'email' => 'rahmaarifinjesikametania@gmail.com',
            'password' => \Illuminate\Support\Facades\Hash::make('Jesica123@'),
            'role' => 'admin',
            'phone' => '+62 812 3456 7890',
            'occupation' => 'CEO, Tech Innovations',
            'address' => 'Jl. Sudirman No. 123, Jakarta Selatan, 12190',
        ]);

        User::create([
            'name' => 'Customer User',
            'email' => 'user@example.com',
            'password' => \Illuminate\Support\Facades\Hash::make('password123'),
            'role' => 'user',
            'phone' => '+62 877 6543 2100',
            'occupation' => 'Designer',
            'address' => 'Jl. Thamrin No. 45, Jakarta Pusat, 10110',
        ]);

        // 2. Seed Cars
        \App\Models\Car::create([
            'name' => 'Porsche 911 Carrera',
            'brand' => 'Porsche',
            'type' => 'Mewah',
            'transmission' => 'Otomatis',
            'fuel_type' => 'Bensin',
            'price_per_day' => 340000,
            'status' => 'available',
            'image_url' => 'https://lh3.googleusercontent.com/aida-public/AB6AXuAmZJwX9HALduF9cKW_9r1FX0fb9wnG19XIslJbgp98yGwXW1QEwAiPNgv7tRYrEiK3o8EYdIKzxu3b0pbJWoCQMZ5oDNacSeIvBLhOYG_l5IX0cslvm2VjMgDx4vZMaTrJazcvSLxOYYb8N0goe5gpRPOIa049kcub7j21mA3_vGZCt0OgEWqtsvKLuqG2CsyQ6-qNQSiDYkGqvIil4QZK_949zEGXu9JTVLSoDmKmQnxRebLMI33fEhlPVwcNjvG71GMtgll5BV4',
            'description' => 'Porsche 911 Carrera legendaris dengan performa luar biasa dan kemewahan yang tak tertandingi.'
        ]);

        \App\Models\Car::create([
            'name' => 'BMW M4 Coupe',
            'brand' => 'BMW',
            'type' => 'Sport',
            'transmission' => 'Semi-Auto',
            'fuel_type' => 'Bensin',
            'price_per_day' => 500000,
            'status' => 'available',
            'image_url' => 'https://lh3.googleusercontent.com/aida-public/AB6AXuDeNMiv2GiR-ZCxsD67uplkSsAtXCblMeE1tGyqQAjsbHE9_2La2ul5-6NHe8r5vmfFMH384w7DH1u4O4M6w6-J8B0FCxcRCyGF5_-giQVORbqGjRxrx05Yzetbley8GU_z6qxvux2-Fn0XvALFjykU8qbbQzxSSKHAi54WfgoKetXyWaRIWbjSq6tK9Ab1Lm8VLrb4sUI7GH9yZnI7J6JL7W2iNQRmX1N8I9LIOZXa7FfCQWSYOxE2PHfm41bHx_UZAoHWkO8ALbM',
            'description' => 'BMW M4 Coupe dengan akselerasi instan dan desain eksterior yang agresif.'
        ]);

        \App\Models\Car::create([
            'name' => 'Tesla Model S Plaid',
            'brand' => 'Tesla',
            'type' => 'Sedan',
            'transmission' => 'Otomatis',
            'fuel_type' => 'Listrik',
            'price_per_day' => 700000,
            'status' => 'available',
            'image_url' => 'https://lh3.googleusercontent.com/aida-public/AB6AXuBIacGVrCXfEJFIOGDvCA8X7EEYHQICmfh8yt9Ee7_5NDQ1PPqgs87TOPtdZ3ApxgXWKhDI_tQgUGpmn4p71rbtMIsKz9jeNg0G5_gY9nDczMl8doEPvbR1Zkmjz-lZsuMYUGgJLVocKBM7MEmI2j_7wQhszzjd4PFgLKlFfXSujl-VBtMXYz8Xcupyf1cW15umF7tSffpbqZ266bpqFtOOu132bX3Ku11hcXfVEFZA8O9RCVL_1hq5_XHVRgozy676k1oq8_Myijc',
            'description' => 'Tesla Model S Plaid bertenaga listrik murni dengan akselerasi 0-100 km/j tercepat di dunia.'
        ]);
    }
}
