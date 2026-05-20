<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use App\Models\User;

class UserController extends Controller
{
    /**
     * Display a listing of all users (Admin only).
     */
    public function index(Request $request)
    {
        return response()->json(User::all());
    }

    /**
     * Display the specified user profile.
     */
    public function show(Request $request)
    {
        return response()->json($request->user());
    }

    /**
     * Update the user profile in storage.
     */
    public function update(Request $request)
    {
        $user = $request->user();

        $validated = $request->validate([
            'name' => 'sometimes|required|string|max:255',
            'email' => 'sometimes|required|string|email|max:255|unique:users,email,' . $user->id,
            'password' => 'nullable|string|min:6',
            'phone' => 'nullable|string|max:255',
            'occupation' => 'nullable|string|max:255',
            'address' => 'nullable|string',
            'avatar' => 'nullable|string', // Simple profile picture URL/Base64
        ]);

        if (isset($validated['password']) && !empty($validated['password'])) {
            $validated['password'] = Hash::make($validated['password']);
        } else {
            unset($validated['password']);
        }

        $user->update($validated);

        return response()->json([
            'message' => 'Profil berhasil diperbarui.',
            'user' => $user
        ]);
    }

    /**
     * Remove the specified user from storage (Admin only).
     */
    public function destroy($id)
    {
        $user = User::findOrFail($id);

        // Prevent admin from deleting themselves
        if ($user->id === auth()->id()) {
            return response()->json([
                'message' => 'Anda tidak dapat menghapus akun Anda sendiri.'
            ], 400);
        }

        $user->delete();

        return response()->json([
            'message' => 'Pengguna berhasil dihapus.'
        ]);
    }
}
