<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Attributes\Fillable;

#[Fillable(['name', 'brand', 'type', 'transmission', 'fuel_type', 'price_per_day', 'status', 'image_url', 'description'])]
class Car extends Model
{
    /**
     * Relasi ke Booking
     */
    public function bookings()
    {
        return $this->hasMany(Booking::class);
    }
}
