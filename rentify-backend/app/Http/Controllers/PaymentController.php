<?php

namespace App\Http\Controllers;

use App\Models\Payment;
use App\Models\Booking;
use Illuminate\Http\Request;

class PaymentController extends Controller
{
    /**
     * Display a listing of payments.
     */
    public function index(Request $request)
    {
        $user = $request->user();

        if ($user->role === 'admin') {
            $payments = Payment::with('booking.user', 'booking.car')->orderBy('created_at', 'desc')->get();
        } else {
            $payments = Payment::whereHas('booking', function ($query) use ($user) {
                $query->where('user_id', $user->id);
            })->with('booking.car')->orderBy('created_at', 'desc')->get();
        }

        return response()->json($payments);
    }

    /**
     * Store a newly created payment.
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'booking_id' => 'required|exists:bookings,id',
            'payment_method' => 'required|string|max:255',
            'amount' => 'required|numeric|min:0',
            'proof_of_payment' => 'nullable|string', // accepts URL or base64 string
        ]);

        $booking = Booking::findOrFail($validated['booking_id']);

        // Check if booking belongs to user or is admin
        if ($booking->user_id !== $request->user()->id && $request->user()->role !== 'admin') {
            return response()->json(['message' => 'Unauthorized.'], 403);
        }

        // Create the payment record
        $payment = Payment::create([
            'booking_id' => $validated['booking_id'],
            'payment_method' => $validated['payment_method'],
            'amount' => $validated['amount'],
            'status' => 'approved', // Auto-approved for simple client experience
            'proof_of_payment' => $validated['proof_of_payment'] ?? 'https://via.placeholder.com/150',
        ]);

        // Confirm the booking status
        $booking->update(['status' => 'confirmed']);

        return response()->json([
            'message' => 'Pembayaran berhasil dikonfirmasi.',
            'payment' => $payment
        ], 201);
    }
}
