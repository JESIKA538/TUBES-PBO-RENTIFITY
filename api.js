const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.hostname === '' || window.location.protocol === 'file:'
    ? 'http://127.0.0.1:8080/api'
    : 'https://tubes-pbo-rentifity-production-8bbb.up.railway.app/api';

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

        let data = {};
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            try {
                data = await response.json();
            } catch (e) {
                console.error("Failed to parse JSON response", e);
            }
        }
        
        if (!response.ok) {
            throw new Error(data.message || `Terjadi kesalahan pada server (Status: ${response.status}).`);
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
        if (data.token) {
            localStorage.setItem('rentify_token', data.token);
            localStorage.setItem('rentify_user', JSON.stringify(data.user));
        }
        return data;
    },

    async register(name, email, password, phone = '', occupation = '', address = '') {
        const data = await apiFetch('/register', {
            method: 'POST',
            body: JSON.stringify({ name, email, password, phone, occupation, address }),
        });
        if (data.token) {
            localStorage.setItem('rentify_token', data.token);
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

    async create(carId, startDate, endDate, notes = '', deliveryOption = 'pickup', deliveryAddress = '') {
        return await apiFetch('/bookings', {
            method: 'POST',
            body: JSON.stringify({ car_id: carId, start_date: startDate, end_date: endDate, notes }),
        });
    },

    async getReports() {
        return await apiFetch('/reports');
    },

    async requestReturn(bookingId) {
        return await apiFetch(`/bookings/${bookingId}/return`, {
            method: 'PUT'
        });
    },

    async confirmReturn(bookingId) {
        return await apiFetch(`/bookings/${bookingId}/confirm-return`, {
            method: 'PUT'
        });
    }
};

// Notifications Helpers
const NotificationsAPI = {
    async getAll() {
        return await apiFetch('/notifications');
    },
    async markAsRead(id) {
        return await apiFetch(`/notifications/${id}/read`, {
            method: 'PUT'
        });
    }
};

// Payments Helpers
const PaymentsAPI = {
    async getAll() {
        return await apiFetch('/payments');
    },

    async create(bookingId, paymentMethod, amount, proofOfPayment = '', paymentChannel = '') {
        return await apiFetch('/payments', {
            method: 'POST',
            body: JSON.stringify({
                booking_id: bookingId,
                payment_method: paymentMethod,
                payment_channel: paymentChannel,
                amount: amount,
                proof_of_payment: proofOfPayment
            }),
        });
    },

    async updateStatus(paymentId, status) {
        return await apiFetch(`/payments/${paymentId}/status`, {
            method: 'PUT',
            body: JSON.stringify({ status }),
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
        const result = await apiFetch('/users/profile', {
            method: 'PUT',
            body: JSON.stringify(profileData),
        });
        
        const user = result.user || result;
        if (user && user.id) {
            localStorage.setItem('rentify_user', JSON.stringify(user));
            
            // Sync with rentify_saved_accounts if exists
            let savedAccounts = localStorage.getItem('rentify_saved_accounts');
            if (savedAccounts) {
                try {
                    let accounts = JSON.parse(savedAccounts);
                    const idx = accounts.findIndex(acc => acc.id === user.id || acc.email === user.email);
                    if (idx !== -1) {
                        accounts[idx].email = user.email;
                        accounts[idx].name = user.name;
                        accounts[idx].avatar = user.avatar;
                        localStorage.setItem('rentify_saved_accounts', JSON.stringify(accounts));
                    }
                } catch (e) {
                    console.error("Failed to sync saved accounts", e);
                }
            }
        }
        if (result.token) {
            localStorage.setItem('rentify_token', result.token);
        }
        return result;
    },

    async changePassword(passwordData) {
        const result = await apiFetch('/users/password', {
            method: 'PUT',
            body: JSON.stringify({
                old_password: passwordData.oldPassword,
                new_password: passwordData.newPassword
            }) // sending as snake_case per spring boot Jackson configuration
        });

        // Sync new password with rentify_saved_accounts
        const currentUser = AuthAPI.getUser();
        if (currentUser) {
            let savedAccounts = localStorage.getItem('rentify_saved_accounts');
            if (savedAccounts) {
                try {
                    let accounts = JSON.parse(savedAccounts);
                    const idx = accounts.findIndex(acc => acc.email === currentUser.email);
                    if (idx !== -1) {
                        accounts[idx].password = passwordData.newPassword;
                        localStorage.setItem('rentify_saved_accounts', JSON.stringify(accounts));
                    }
                } catch (e) {
                    console.error("Failed to sync new password", e);
                }
            }
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


const ReviewsAPI = {
    async create(bookingId, rating, comment) {
        return await apiFetch('/reviews', {
            method: 'POST',
            body: JSON.stringify({ booking_id: bookingId, rating, comment })
        });
    },
    async getByCar(carId) {
        return await apiFetch(`/cars/${carId}/reviews`);
    }
};

const PromosAPI = {
    async validate(code) {
        return await apiFetch(`/promos/validate?code=${encodeURIComponent(code)}`);
    }
};
