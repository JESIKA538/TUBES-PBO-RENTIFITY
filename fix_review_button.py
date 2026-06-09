import os

file_path = r"c:\TUBES PBO RENTIFITY\booking-mobil.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Inject the actionBtn logic
old_js = """                        } else if (booking.status === 'confirmed') {
                            actionBtn = `<button onclick="requestCarReturn(${booking.id})"
                                class="w-full flex items-center justify-center gap-2 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-label-md font-bold active:scale-[0.98] transition-all shadow-sm">
                                <span class="material-symbols-outlined text-[18px]">restart_alt</span>
                                Kembalikan Mobil
                               </button>`;
                        }"""

new_js = old_js + """ else if (booking.status === 'completed') {
                            actionBtn = `<button onclick="openReviewModal(${booking.id}, ${car.id}, '${carName}')"
                                class="w-full flex items-center justify-center gap-2 py-2.5 bg-yellow-500 hover:bg-yellow-600 text-white rounded-lg font-label-md font-bold active:scale-[0.98] transition-all shadow-sm">
                                <span class="material-symbols-outlined text-[18px]">star</span>
                                Beri Ulasan
                               </button>`;
                        }"""
html = html.replace(old_js, new_js)

# Inject lateFee display logic
old_price = """                                <div class="mt-4 pt-4 border-t border-outline-variant/30 flex items-center justify-between">
                                    <span class="font-body-md text-on-surface-variant">Total</span>
                                    <span class="font-headline-sm text-primary font-bold">${totalFmt}</span>
                                </div>"""

new_price = """                                ${booking.lateFee > 0 ? `
                                <div class="mt-2 pt-2 border-t border-outline-variant/30 flex items-center justify-between text-red-600">
                                    <span class="font-body-sm">Denda Telat</span>
                                    <span class="font-bold text-sm">Rp ${Number(booking.lateFee).toLocaleString('id-ID')}</span>
                                </div>` : ''}
                                <div class="mt-4 pt-4 border-t border-outline-variant/30 flex items-center justify-between">
                                    <span class="font-body-md text-on-surface-variant">Total</span>
                                    <span class="font-headline-sm text-primary font-bold">${totalFmt}</span>
                                </div>"""
html = html.replace(old_price, new_price)

# Inject the Review Modal and Scripts if not exists
if "openReviewModal" not in html:
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
    html = html.replace("</body>", modal_html + "\n</body>")
    
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
                alert(e.message || "Gagal mengirim ulasan, mungkin Anda sudah pernah mengulas pesanan ini.");
            }
        }
"""
    html = html.replace("async function loadBookings() {", script_js + "\n        async function loadBookings() {")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Review button injected.")
