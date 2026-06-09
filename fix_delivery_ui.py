import os

file_path = r"c:\TUBES PBO RENTIFITY\booking-mobil.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Inject UI
old_ui = """                            <div class="flex flex-col gap-2">
                                <label class="font-label-md text-label-md text-on-surface-variant">Tanggal Selesai</label>
                                <div
                                    class="flex items-center gap-2 bg-surface-container-low border border-outline-variant rounded-lg p-3">
                                    <span class="material-symbols-outlined text-primary">event_note</span>
                                    <input id="booking-end-date"
                                        class="bg-transparent border-none w-full font-body-sm text-body-sm focus:ring-0"
                                        type="date" min="" />
                                </div>
                            </div>"""

new_ui = old_ui + """
                            <!-- Opsi Pengiriman -->
                            <div class="flex flex-col gap-2 mt-2">
                                <label class="font-label-md text-label-md text-on-surface-variant">Opsi Pengambilan</label>
                                <div class="grid grid-cols-2 gap-3">
                                    <label class="flex items-center gap-2 p-3 border border-outline-variant rounded-lg cursor-pointer hover:bg-surface-container-low transition-colors">
                                        <input type="radio" name="deliveryOption" value="pickup" checked class="text-primary focus:ring-primary" onchange="document.getElementById('addressContainer').classList.add('hidden')" />
                                        <div class="flex flex-col">
                                            <span class="font-label-sm text-on-surface">Ambil Sendiri</span>
                                            <span class="text-[10px] text-on-surface-variant">Gratis</span>
                                        </div>
                                    </label>
                                    <label class="flex items-center gap-2 p-3 border border-outline-variant rounded-lg cursor-pointer hover:bg-surface-container-low transition-colors">
                                        <input type="radio" name="deliveryOption" value="delivery" class="text-primary focus:ring-primary" onchange="document.getElementById('addressContainer').classList.remove('hidden')" />
                                        <div class="flex flex-col">
                                            <span class="font-label-sm text-on-surface">Diantar</span>
                                            <span class="text-[10px] text-on-surface-variant">+ Biaya Kurir</span>
                                        </div>
                                    </label>
                                </div>
                            </div>
                            <div id="addressContainer" class="hidden flex flex-col gap-2">
                                <label class="font-label-md text-label-md text-on-surface-variant">Alamat Pengiriman</label>
                                <textarea id="deliveryAddress" rows="2" class="w-full p-3 bg-surface-container-low border border-outline-variant rounded-lg font-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-primary" placeholder="Ketik alamat lengkap Anda..."></textarea>
                            </div>
"""

html = html.replace(old_ui, new_ui)

# Inject JS logic
old_js = """                    const pickupNote = pickupLocation
                        ? `Penjemputan: ${pickupLocation}`
                        : 'Sewa Mobil Premium';
                    const result = await BookingsAPI.create(carId, startDate, endDate, pickupNote);"""

new_js = """                    const pickupNote = pickupLocation
                        ? `Penjemputan: ${pickupLocation}`
                        : 'Sewa Mobil Premium';
                    
                    const deliveryOption = document.querySelector('input[name="deliveryOption"]:checked') ? document.querySelector('input[name="deliveryOption"]:checked').value : 'pickup';
                    const deliveryAddress = document.getElementById('deliveryAddress') ? document.getElementById('deliveryAddress').value : '';
                        
                    const result = await BookingsAPI.create(carId, startDate, endDate, pickupNote, deliveryOption, deliveryAddress);"""

html = html.replace(old_js, new_js)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Delivery UI fixed.")
