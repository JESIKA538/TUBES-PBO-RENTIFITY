import os

BASE_DIR = r"c:\TUBES PBO RENTIFITY"

# 1. Update riwayat.html (Add Beri Ulasan Button)
riwayat_path = os.path.join(BASE_DIR, "riwayat.html")
with open(riwayat_path, "r") as f:
    r_html = f.read()

if "openReviewModal" not in r_html:
    btn_logic = """
                    ${b.status === 'completed' && !b.hasReview ? `
                        <button onclick="openReviewModal(${b.id}, ${b.car.id}, '${b.car.name}')" class="w-full py-2 bg-yellow-500 hover:bg-yellow-600 text-white font-bold text-sm rounded-lg transition-colors flex items-center justify-center gap-2">
                            <span class="material-symbols-outlined text-sm">star</span> Beri Ulasan
                        </button>
                    ` : ''}
                    ${b.lateFee > 0 ? `
                        <div class="mt-2 p-2 bg-red-50 border border-red-200 rounded-lg flex items-center justify-between text-sm">
                            <span class="text-red-700 font-bold">Denda Keterlambatan:</span>
                            <span class="text-red-700 font-bold">${formatRupiah(b.lateFee)}</span>
                        </div>
                    ` : ''}
"""
    r_html = r_html.replace("</div>\n                </div>\n            </div>`;", btn_logic + "\n                </div>\n            </div>`;")
    
    modal_html = """
    <!-- Review Modal -->
    <div id="reviewModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 hidden flex items-center justify-center opacity-0 transition-opacity">
        <div class="bg-white w-full max-w-md rounded-2xl p-6 transform scale-95 transition-transform duration-300">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-xl font-bold text-gray-900 font-heading">Beri Ulasan</h3>
                <button onclick="closeReviewModal()" class="text-gray-400 hover:text-gray-600">
                    <span class="material-symbols-outlined">close</span>
                </button>
            </div>
            <p id="reviewCarName" class="text-sm text-gray-600 mb-4 font-bold"></p>
            <div class="flex justify-center gap-2 mb-6" id="starContainer">
                <span class="material-symbols-outlined text-4xl cursor-pointer text-gray-300 hover:text-yellow-400 transition-colors" onclick="setRating(1)">star</span>
                <span class="material-symbols-outlined text-4xl cursor-pointer text-gray-300 hover:text-yellow-400 transition-colors" onclick="setRating(2)">star</span>
                <span class="material-symbols-outlined text-4xl cursor-pointer text-gray-300 hover:text-yellow-400 transition-colors" onclick="setRating(3)">star</span>
                <span class="material-symbols-outlined text-4xl cursor-pointer text-gray-300 hover:text-yellow-400 transition-colors" onclick="setRating(4)">star</span>
                <span class="material-symbols-outlined text-4xl cursor-pointer text-gray-300 hover:text-yellow-400 transition-colors" onclick="setRating(5)">star</span>
            </div>
            <textarea id="reviewComment" rows="3" class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary/30 mb-4" placeholder="Bagaimana pengalaman Anda?"></textarea>
            <button onclick="submitReview()" class="w-full py-3 bg-primary hover:bg-primary-dark text-white font-bold rounded-xl transition-all">Kirim Ulasan</button>
        </div>
    </div>
"""
    r_html = r_html.replace("</body>", modal_html + "\n</body>")
    
    script_js = """
        let currentReviewBookingId = null;
        let currentRating = 5;

        function openReviewModal(bookingId, carId, carName) {
            currentReviewBookingId = bookingId;
            document.getElementById('reviewCarName').textContent = `Menyewa: ${carName}`;
            setRating(5);
            document.getElementById('reviewComment').value = '';
            
            const modal = document.getElementById('reviewModal');
            modal.classList.remove('hidden');
            setTimeout(() => {
                modal.classList.remove('opacity-0');
                modal.querySelector('div').classList.remove('scale-95');
            }, 10);
        }

        function closeReviewModal() {
            const modal = document.getElementById('reviewModal');
            modal.classList.add('opacity-0');
            modal.querySelector('div').classList.add('scale-95');
            setTimeout(() => {
                modal.classList.add('hidden');
            }, 300);
        }

        function setRating(rating) {
            currentRating = rating;
            const stars = document.getElementById('starContainer').children;
            for(let i=0; i<5; i++) {
                if(i < rating) {
                    stars[i].classList.remove('text-gray-300');
                    stars[i].classList.add('text-yellow-400');
                } else {
                    stars[i].classList.remove('text-yellow-400');
                    stars[i].classList.add('text-gray-300');
                }
            }
        }

        async function submitReview() {
            const comment = document.getElementById('reviewComment').value;
            try {
                await ReviewsAPI.create(currentReviewBookingId, currentRating, comment);
                alert("Ulasan berhasil dikirim! Terima kasih.");
                closeReviewModal();
                loadBookings();
            } catch(e) {
                alert(e.message || "Gagal mengirim ulasan");
            }
        }
"""
    r_html = r_html.replace("function renderBookings(bookings) {", script_js + "\n        function renderBookings(bookings) {")
    with open(riwayat_path, "w") as f:
        f.write(r_html)

# 2. Update detail-mobil.html (Add Review List)
detail_path = os.path.join(BASE_DIR, "detail-mobil.html")
with open(detail_path, "r") as f:
    det_html = f.read()

if "id=\"reviewsList\"" not in det_html:
    review_ui = """
                    <!-- Reviews Section -->
                    <div class="bg-white rounded-3xl p-6 md:p-8 shadow-sm border border-gray-100 mb-8 fade-up" style="animation-delay: 0.2s;">
                        <h2 class="text-xl font-heading font-bold text-gray-900 mb-6 flex items-center gap-2">
                            <span class="material-symbols-outlined text-primary">star</span> Ulasan Pengguna
                        </h2>
                        <div id="reviewsList" class="space-y-6">
                            <div class="text-center py-6 text-gray-500">Memuat ulasan...</div>
                        </div>
                    </div>
"""
    det_html = det_html.replace("</main>", review_ui + "\n    </main>")
    
    script_to_add = """
        async function loadReviews(carId) {
            try {
                const reviews = await ReviewsAPI.getByCar(carId);
                const list = document.getElementById('reviewsList');
                if(!reviews || reviews.length === 0) {
                    list.innerHTML = '<div class="text-center py-6 text-gray-500">Belum ada ulasan untuk mobil ini.</div>';
                    return;
                }
                
                list.innerHTML = reviews.map(r => {
                    let stars = '';
                    for(let i=0; i<5; i++) {
                        stars += `<span class="material-symbols-outlined text-sm ${i < r.rating ? 'text-yellow-400' : 'text-gray-300'}">star</span>`;
                    }
                    const date = new Date(r.createdAt || r.created_at).toLocaleDateString('id-ID', {day: 'numeric', month: 'long', year: 'numeric'});
                    
                    return `
                        <div class="border-b border-gray-100 last:border-0 pb-6 last:pb-0">
                            <div class="flex items-center gap-3 mb-2">
                                <img src="${r.user.avatar || 'jeje_profile.png'}" class="w-10 h-10 rounded-full object-cover" onerror="this.onerror=null; this.src='https://api.dicebear.com/7.x/initials/svg?seed='+r.user.name" />
                                <div>
                                    <p class="font-bold text-sm text-gray-900">${r.user.name}</p>
                                    <p class="text-xs text-gray-500">${date}</p>
                                </div>
                            </div>
                            <div class="flex mb-2">${stars}</div>
                            <p class="text-gray-700 text-sm leading-relaxed">${r.comment || ''}</p>
                        </div>
                    `;
                }).join('');
            } catch(e) {
                console.error(e);
            }
        }
"""
    det_html = det_html.replace("async function loadCarDetails() {", script_to_add + "\n        async function loadCarDetails() {")
    det_html = det_html.replace("document.getElementById('carPrice').textContent = formatRupiah(car.pricePerDay);", "document.getElementById('carPrice').textContent = formatRupiah(car.pricePerDay);\n                loadReviews(carId);")
    
    with open(detail_path, "w") as f:
        f.write(det_html)

print("Frontend reviews UI injected successfully.")
