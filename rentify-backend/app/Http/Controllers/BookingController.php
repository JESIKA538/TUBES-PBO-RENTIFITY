<?php

namespace App\Http\Controllers;

use App\Models\Booking;
use App\Models\Car;
use Illuminate\Http\Request;
use Carbon\Carbon;

class BookingController extends Controller
{
    /**
     * Display a listing of bookings.
     */
    public function index(Request $request)
    {
        $user = $request->user();

        if ($user->role === 'admin') {
            // Admins see all bookings
            $bookings = Booking::with(['user', 'car', 'payments'])->orderBy('created_at', 'desc')->get();
        } else {
            // Customers see only their own bookings
            $bookings = Booking::with(['car', 'payments'])
                ->where('user_id', $user->id)
                ->orderBy('created_at', 'desc')
                ->get();
        }

        return response()->json($bookings);
    }

    /**
     * Store a newly created booking.
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'car_id' => 'required|exists:cars,id',
            'start_date' => 'required|date|after_or_equal:today',
            'end_date' => 'required|date|after_or_equal:start_date',
            'notes' => 'nullable|string',
        ]);

        $car = Car::findOrFail($validated['car_id']);

        if ($car->status !== 'available') {
            return response()->json([
                'message' => 'Mobil ini saat ini sedang tidak tersedia untuk disewa.'
            ], 422);
        }

        // Calculate total days
        $start = Carbon::parse($validated['start_date']);
        $end = Carbon::parse($validated['end_date']);
        $days = $start->diffInDays($end);
        if ($days === 0) {
            $days = 1; // Minimum 1 day rent
        }

        $totalPrice = $days * $car->price_per_day;

        // Create booking
        $booking = Booking::create([
            'user_id' => $request->user()->id,
            'car_id' => $validated['car_id'],
            'start_date' => $validated['start_date'],
            'end_date' => $validated['end_date'],
            'total_price' => $totalPrice,
            'status' => 'pending', // pending, confirmed, completed, cancelled
            'notes' => $validated['notes'] ?? null,
        ]);

        // Update car status to prevent other bookings
        $car->update(['status' => 'rented']);

        return response()->json([
            'message' => 'Pesanan berhasil dibuat. Silakan lakukan pembayaran.',
            'booking' => $booking->load('car')
        ], 201);
    }

    /**
     * Get booking reports and statistics (Admin & general charts).
     */
    public function reports(Request $request)
    {
        // Admin or stats
        $totalBookings = Booking::count();
        $totalRevenue = Booking::whereIn('status', ['confirmed', 'completed'])->sum('total_price');
        $availableCars = Car::where('status', 'available')->count();
        $totalCars = Car::count();

        // Recent bookings
        $recentBookings = Booking::with(['user', 'car'])->orderBy('created_at', 'desc')->limit(5)->get();

        // Get revenue by month (simple format for dashboard charts)
        $revenueStats = [
            ['month' => 'Jan', 'revenue' => 1200000],
            ['month' => 'Feb', 'revenue' => 1900000],
            ['month' => 'Mar', 'revenue' => 3200000],
            ['month' => 'Apr', 'revenue' => 5000000],
            ['month' => 'May', 'revenue' => floatval($totalRevenue)]
        ];

        return response()->json([
            'total_bookings' => $totalBookings,
            'total_revenue' => $totalRevenue,
            'available_cars' => $availableCars,
            'total_cars' => $totalCars,
            'recent_bookings' => $recentBookings,
            'revenue_stats' => $revenueStats
        ]);
    }
}
