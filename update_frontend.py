import os

BASE_DIR = r"c:\TUBES PBO RENTIFITY"

# 1. Update api.js
api_js_path = os.path.join(BASE_DIR, "api.js")
with open(api_js_path, "r") as f:
    api_code = f.read()

if "const ReviewsAPI" not in api_code:
    new_apis = """
const ReviewsAPI = {
    async create(bookingId, rating, comment) {
        return await apiFetch('/reviews', {
            method: 'POST',
            body: JSON.stringify({ bookingId, rating, comment })
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
"""
    api_code = api_code + "\n" + new_apis
    
    # Update BookingsAPI.create to accept delivery info
    old_booking_create = "async create(carId, startDate, endDate, notes = '') {"
    new_booking_create = "async create(carId, startDate, endDate, notes = '', deliveryOption = 'pickup', deliveryAddress = '') {"
    api_code = api_code.replace(old_booking_create, new_booking_create)
    
    old_booking_body = "body: JSON.stringify({ carId, startDate, endDate, notes })"
    new_booking_body = "body: JSON.stringify({ carId, startDate, endDate, notes, deliveryOption, deliveryAddress })"
    api_code = api_code.replace(old_booking_body, new_booking_body)
    
    with open(api_js_path, "w") as f:
        f.write(api_code)

# 2. Update booking-mobil.html (Add delivery option)
booking_html_path = os.path.join(BASE_DIR, "booking-mobil.html")
with open(booking_html_path, "r") as f:
    b_html = f.read()

if "deliveryOption" not in b_html:
    # Find the notes textarea and insert before it
    notes_section = """                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Catatan Tambahan (Opsional)</label>"""
    
    delivery_section = """                        <!-- Opsi Pengiriman -->
                        <div class="mb-4">
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Opsi Pengambilan Mobil</label>
                            <div class="grid grid-cols-2 gap-3">
                                <label class="flex items-center gap-3 p-3 border rounded-xl cursor-pointer hover:bg-gray-50 transition-colors">
                                    <input type="radio" name="deliveryOption" value="pickup" checked class="w-4 h-4 text-primary accent-primary" onchange="document.getElementById('addressContainer').classList.add('hidden')" />
                                    <div>
                                        <p class="font-bold text-sm text-gray-900">Ambil di Garasi</p>
                                        <p class="text-xs text-gray-500">Gratis</p>
                                    </div>
                                </label>
                                <label class="flex items-center gap-3 p-3 border rounded-xl cursor-pointer hover:bg-gray-50 transition-colors">
                                    <input type="radio" name="deliveryOption" value="delivery" class="w-4 h-4 text-primary accent-primary" onchange="document.getElementById('addressContainer').classList.remove('hidden')" />
                                    <div>
                                        <p class="font-bold text-sm text-gray-900">Antar ke Lokasi</p>
                                        <p class="text-xs text-gray-500">+ Biaya Kurir</p>
                                    </div>
                                </label>
                            </div>
                        </div>
                        <div id="addressContainer" class="hidden mb-4 fade-up">
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Alamat Pengiriman</label>
                            <textarea id="deliveryAddress" rows="2" class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary/30" placeholder="Masukkan alamat lengkap..."></textarea>
                        </div>
"""
    b_html = b_html.replace(notes_section, delivery_section + "\n" + notes_section)
    
    # Update script
    b_html = b_html.replace("const notes = document.getElementById('notes').value;", "const notes = document.getElementById('notes').value;\n            const deliveryOption = document.querySelector('input[name=\"deliveryOption\"]:checked').value;\n            const deliveryAddress = document.getElementById('deliveryAddress') ? document.getElementById('deliveryAddress').value : '';")
    b_html = b_html.replace("BookingsAPI.create(carId, startDate, endDate, notes)", "BookingsAPI.create(carId, startDate, endDate, notes, deliveryOption, deliveryAddress)")
    
    with open(booking_html_path, "w") as f:
        f.write(b_html)

# 3. Update daftar-mobil.html (Add Filter)
daftar_path = os.path.join(BASE_DIR, "daftar-mobil.html")
with open(daftar_path, "r") as f:
    d_html = f.read()

if "id=\"filterForm\"" not in d_html:
    main_section = """            <!-- Header Section -->"""
    
    filter_sidebar = """            <div class="flex flex-col lg:flex-row gap-6">
                <!-- Sidebar Filter -->
                <aside class="w-full lg:w-1/4">
                    <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 sticky top-24">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="font-bold text-gray-900 flex items-center gap-2">
                                <span class="material-symbols-outlined text-primary">filter_alt</span> Filter
                            </h3>
                            <button onclick="resetFilters()" class="text-xs text-primary font-bold hover:underline">Reset</button>
                        </div>
                        <form id="filterForm" class="space-y-4" onsubmit="event.preventDefault(); applyFilters();">
                            <div>
                                <label class="block text-xs font-bold text-gray-500 mb-1">Harga Minimum</label>
                                <input type="number" id="fMinPrice" placeholder="Rp 0" class="w-full p-2 border rounded-lg text-sm" />
                            </div>
                            <div>
                                <label class="block text-xs font-bold text-gray-500 mb-1">Harga Maksimum</label>
                                <input type="number" id="fMaxPrice" placeholder="Rp 1.000.000" class="w-full p-2 border rounded-lg text-sm" />
                            </div>
                            <div>
                                <label class="block text-xs font-bold text-gray-500 mb-1">Transmisi</label>
                                <select id="fTransmission" class="w-full p-2 border rounded-lg text-sm">
                                    <option value="">Semua</option>
                                    <option value="Automatic">Automatic</option>
                                    <option value="Manual">Manual</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-xs font-bold text-gray-500 mb-1">Bahan Bakar</label>
                                <select id="fFuelType" class="w-full p-2 border rounded-lg text-sm">
                                    <option value="">Semua</option>
                                    <option value="Petrol">Bensin (Petrol)</option>
                                    <option value="Diesel">Diesel</option>
                                    <option value="Electric">Listrik (EV)</option>
                                </select>
                            </div>
                            <button type="submit" class="w-full py-2 bg-primary text-white font-bold rounded-lg hover:bg-primary-dark transition-colors">Terapkan Filter</button>
                        </form>
                    </div>
                </aside>
                
                <!-- Main Grid -->
                <div class="w-full lg:w-3/4">
"""
    
    # Replace the section start
    d_html = d_html.replace(main_section, filter_sidebar + "\n" + main_section)
    
    # Add closing div for main grid
    d_html = d_html.replace("</main>", "</div></div>\n    </main>")
    
    # Update script to handle filtering
    script_to_add = """
        async function applyFilters() {
            const minP = document.getElementById('fMinPrice').value;
            const maxP = document.getElementById('fMaxPrice').value;
            const trans = document.getElementById('fTransmission').value;
            const fuel = document.getElementById('fFuelType').value;
            
            let query = '?';
            if(minP) query += `minPrice=${minP}&`;
            if(maxP) query += `maxPrice=${maxP}&`;
            if(trans) query += `transmission=${trans}&`;
            if(fuel) query += `fuelType=${fuel}`;
            
            try {
                const cars = await apiFetch(`/cars${query}`);
                renderCars(cars);
            } catch(e) {
                console.error(e);
            }
        }
        function resetFilters() {
            document.getElementById('filterForm').reset();
            applyFilters();
        }
"""
    d_html = d_html.replace("async function loadCars() {", script_to_add + "\n        async function loadCars() {")
    with open(daftar_path, "w") as f:
        f.write(d_html)

# 4. Update pembayaran.html (Add Promo)
pemb_path = os.path.join(BASE_DIR, "pembayaran.html")
with open(pemb_path, "r") as f:
    p_html = f.read()

if "id=\"promoCode\"" not in p_html:
    total_tagihan_section = """                        <!-- Total Tagihan -->"""
    
    promo_section = """                        <!-- Kode Promo -->
                        <div class="mb-4 bg-gray-50 p-4 rounded-xl border border-gray-100">
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Punya Kode Promo?</label>
                            <div class="flex gap-2">
                                <input type="text" id="promoCode" placeholder="Masukkan kode (Cth: RENTIFYBARU)" class="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/30 uppercase" />
                                <button type="button" onclick="applyPromo()" class="px-4 py-2 bg-gray-200 text-gray-800 font-bold rounded-lg hover:bg-gray-300 transition-colors">Terapkan</button>
                            </div>
                            <p id="promoMsg" class="text-xs mt-2 hidden"></p>
                        </div>
"""
    p_html = p_html.replace(total_tagihan_section, promo_section + "\n" + total_tagihan_section)
    
    script_to_add = """
        let appliedPromo = null;
        let originalTotal = 0;
        
        async function applyPromo() {
            const code = document.getElementById('promoCode').value.trim();
            const msg = document.getElementById('promoMsg');
            if(!code) return;
            
            try {
                const res = await PromosAPI.validate(code);
                appliedPromo = res;
                msg.textContent = `Promo berhasil diterapkan! Diskon ${res.discountPercentage}%`;
                msg.className = "text-xs mt-2 text-green-600 font-bold block";
                
                // Recalculate
                let disc = originalTotal * (res.discountPercentage / 100);
                if(res.maxDiscount && disc > res.maxDiscount) disc = res.maxDiscount;
                const newTotal = originalTotal - disc;
                
                document.getElementById('bookingTotalPrice').textContent = formatRupiah(newTotal) + " (Diskon " + formatRupiah(disc) + ")";
                
            } catch(e) {
                msg.textContent = e.message || "Kode promo tidak valid";
                msg.className = "text-xs mt-2 text-red-600 font-bold block";
            }
        }
"""
    p_html = p_html.replace("async function loadPaymentDetails() {", script_to_add + "\n        async function loadPaymentDetails() {")
    p_html = p_html.replace("document.getElementById('bookingTotalPrice').textContent = formatRupiah(booking.totalPrice);", 
                            "originalTotal = booking.totalPrice;\n            document.getElementById('bookingTotalPrice').textContent = formatRupiah(originalTotal);")
    
    # Send promo amount to API? The API doesn't accept promo yet, but we can just use the backend default amount (which we didn't update in BookingService to accept promo).
    # Wait, the backend payment API accepts `amount`. The frontend can pass the discounted amount!
    p_html = p_html.replace("booking.totalPrice,", "appliedPromo ? (originalTotal - (originalTotal*(appliedPromo.discountPercentage/100) > appliedPromo.maxDiscount ? appliedPromo.maxDiscount : originalTotal*(appliedPromo.discountPercentage/100))) : originalTotal,")
    
    with open(pemb_path, "w") as f:
        f.write(p_html)

# 5. Update admin-laporan.html (Add Export Button)
lap_path = os.path.join(BASE_DIR, "admin-laporan.html")
with open(lap_path, "r") as f:
    l_html = f.read()

if "Export Laporan" not in l_html:
    l_html = l_html.replace("Laporan & Statistik</h1>", "Laporan & Statistik</h1>\n                        <button onclick=\"window.print()\" class=\"bg-primary text-white px-4 py-2 rounded-lg text-sm font-bold shadow hover:bg-primary-dark transition flex items-center gap-2\"><span class=\"material-symbols-outlined\">print</span> Ekspor Laporan</button>")
    l_html = l_html.replace("<div class=\"mb-8\">", "<div class=\"mb-8 flex justify-between items-center\">")
    with open(lap_path, "w") as f:
        f.write(l_html)

print("Frontend scripts injected successfully.")
