const API_URL = 'http://127.0.0.1:8000/api';

/**
 * Generic API Fetch wrapper that injects headers and bearer tokens,
 * and handles authentication failures.
 */
async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('rentify_token');
    
    // Set default headers
    const headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        ...options,
        headers,
    };

    try {
        const response = await fetch(`${API_URL}${endpoint}`, config);
        
        // Handle unauthorized (session expired)
        if (response.status === 401) {
            localStorage.removeItem('rentify_token');
            localStorage.removeItem('rentify_user');
            if (!window.location.pathname.endsWith('login.html') && !window.location.pathname.endsWith('register.html')) {
                window.location.href = 'login.html';
            }
            throw new Error('Sesi Anda telah berakhir. Silakan login kembali.');
        }

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Terjadi kesalahan pada server.');
        }
        
        return data;
    } catch (error) {
        console.error(`API Error on ${endpoint}:`, error);
        throw error;
    }
}

// Authentication Helpers
const AuthAPI = {
    async login(email, password) {
        const data = await apiFetch('/login', {
            method: 'POST',
            body: JSON.stringify({ email, password }),
        });
        if (data.access_token) {
            localStorage.setItem('rentify_token', data.access_token);
            localStorage.setItem('rentify_user', JSON.stringify(data.user));
        }
        return data;
    },

    async register(name, email, password, phone = '', occupation = '', address = '') {
        const data = await apiFetch('/register', {
            method: 'POST',
            body: JSON.stringify({ name, email, password, phone, occupation, address }),
        });
        if (data.access_token) {
            localStorage.setItem('rentify_token', data.access_token);
            localStorage.setItem('rentify_user', JSON.stringify(data.user));
        }
        return data;
    },

    async logout() {
        try {
            await apiFetch('/logout', { method: 'POST' });
        } catch (e) {
            console.warn('Logout request failed, clearing local storage anyway.', e);
        }
        localStorage.removeItem('rentify_token');
        localStorage.removeItem('rentify_user');
        window.location.href = 'login.html';
    },

    getUser() {
        const userStr = localStorage.getItem('rentify_user');
        return userStr ? JSON.parse(userStr) : null;
    },

    getToken() {
        return localStorage.getItem('rentify_token');
    },

    checkAuth() {
        const token = this.getToken();
        const user = this.getUser();
        if (!token || !user) {
            if (!window.location.pathname.endsWith('login.html') && !window.location.pathname.endsWith('register.html')) {
                window.location.href = 'login.html';
            }
            return false;
        }
        return true;
    }
};

// Cars Helpers
const CarsAPI = {
    async getAll(filters = {}) {
        const params = new URLSearchParams();
        if (filters.status) params.append('status', filters.status);
        if (filters.search) params.append('search', filters.search);
        if (filters.type) params.append('type', filters.type);
        
        const queryString = params.toString() ? `?${params.toString()}` : '';
        return await apiFetch(`/cars${queryString}`);
    },

    async getById(id) {
        return await apiFetch(`/cars/${id}`);
    },

    // Admin CRUD
    async create(carData) {
        return await apiFetch('/cars', {
            method: 'POST',
            body: JSON.stringify(carData),
        });
    },

    async update(id, carData) {
        return await apiFetch(`/cars/${id}`, {
            method: 'PUT',
            body: JSON.stringify(carData),
        });
    },

    async delete(id) {
        return await apiFetch(`/cars/${id}`, {
            method: 'DELETE',
        });
    }
};

// Bookings Helpers
const BookingsAPI = {
    async getAll() {
        return await apiFetch('/bookings');
    },

    async create(carId, startDate, endDate, notes = '') {
        return await apiFetch('/bookings', {
            method: 'POST',
            body: JSON.stringify({ car_id: carId, start_date: startDate, end_date: endDate, notes }),
        });
    },

    async getReports() {
        return await apiFetch('/reports');
    }
};

// Payments Helpers
const PaymentsAPI = {
    async getAll() {
        return await apiFetch('/payments');
    },

    async create(bookingId, paymentMethod, amount, proofOfPayment = '') {
        return await apiFetch('/payments', {
            method: 'POST',
            body: JSON.stringify({
                booking_id: bookingId,
                payment_method: paymentMethod,
                amount: amount,
                proof_of_payment: proofOfPayment
            }),
        });
    }
};

// User Profile Helpers
const UserAPI = {
    async getProfile() {
        const user = await apiFetch('/user');
        localStorage.setItem('rentify_user', JSON.stringify(user));
        return user;
    },

    async updateProfile(profileData) {
        const result = await apiFetch('/user', {
            method: 'PUT',
            body: JSON.stringify(profileData),
        });
        if (result.user) {
            localStorage.setItem('rentify_user', JSON.stringify(result.user));
        }
        return result;
    },

    async getAll() {
        return await apiFetch('/users');
    },

    async delete(id) {
        return await apiFetch(`/users/${id}`, {
            method: 'DELETE',
        });
    }
};
