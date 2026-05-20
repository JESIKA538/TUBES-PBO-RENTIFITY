<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Attributes\Fillable;

#[Fillable(['user_id', 'car_id', 'start_date', 'end_date', 'total_price', 'status', 'notes'])]
class Booking extends Model
{
    /**
     * Relasi ke User
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    /**
     * Relasi ke Car
     */
    public function car()
    {
        return $this->belongsTo(Car::class);
    }

    /**
     * Relasi ke Payment
     */
    public function payments()
    {
        return $this->hasMany(Payment::class);
    }
}
