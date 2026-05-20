<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Attributes\Fillable;

#[Fillable(['booking_id', 'payment_method', 'amount', 'status', 'proof_of_payment'])]
class Payment extends Model
{
    /**
     * Relasi ke Booking
     */
    public function booking()
    {
        return $this->belongsTo(Booking::class);
    }
}
