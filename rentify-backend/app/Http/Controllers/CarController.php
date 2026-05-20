<?php

namespace App\Http\Controllers;

use App\Models\Car;
use Illuminate\Http\Request;

class CarController extends Controller
{
    /**
     * Display a listing of cars.
     */
    public function index(Request $request)
    {
        $query = Car::query();

        // Filter by availability/status
        if ($request->has('status')) {
            $query->where('status', $request->status);
        }

        // Search by brand or name
        if ($request->has('search')) {
            $search = $request->search;
            $query->where(function($q) use ($search) {
                $q->where('name', 'like', "%{$search}%")
                  ->orWhere('brand', 'like', "%{$search}%");
            });
        }

        // Filter by type
        if ($request->has('type')) {
            $query->where('type', $request->type);
        }

        return response()->json($query->get());
    }

    /**
     * Display the specified car.
     */
    public function show($id)
    {
        $car = Car::find($id);

        if (!$car) {
            return response()->json([
                'message' => 'Mobil tidak ditemukan.'
            ], 404);
        }

        return response()->json($car);
    }

    /**
     * Store a newly created car in storage (Admin only).
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'brand' => 'required|string|max:255',
            'type' => 'required|string|max:255',
            'transmission' => 'required|string|max:255',
            'fuel_type' => 'required|string|max:255',
            'price_per_day' => 'required|numeric|min:0',
            'status' => 'nullable|string|in:available,rented,maintenance',
            'image_url' => 'nullable|string',
            'description' => 'nullable|string',
        ]);

        $car = Car::create($validated);

        return response()->json([
            'message' => 'Mobil berhasil ditambahkan.',
            'car' => $car
        ], 201);
    }

    /**
     * Update the specified car in storage (Admin only).
     */
    public function update(Request $request, $id)
    {
        $car = Car::find($id);

        if (!$car) {
            return response()->json([
                'message' => 'Mobil tidak ditemukan.'
            ], 404);
        }

        $validated = $request->validate([
            'name' => 'sometimes|required|string|max:255',
            'brand' => 'sometimes|required|string|max:255',
            'type' => 'sometimes|required|string|max:255',
            'transmission' => 'sometimes|required|string|max:255',
            'fuel_type' => 'sometimes|required|string|max:255',
            'price_per_day' => 'sometimes|required|numeric|min:0',
            'status' => 'sometimes|required|string|in:available,rented,maintenance',
            'image_url' => 'nullable|string',
            'description' => 'nullable|string',
        ]);

        $car->update($validated);

        return response()->json([
            'message' => 'Mobil berhasil diperbarui.',
            'car' => $car
        ]);
    }

    /**
     * Remove the specified car from storage (Admin only).
     */
    public function destroy($id)
    {
        $car = Car::find($id);

        if (!$car) {
            return response()->json([
                'message' => 'Mobil tidak ditemukan.'
            ], 404);
        }

        $car->delete();

        return response()->json([
            'message' => 'Mobil berhasil dihapus.'
        ]);
    }
}
