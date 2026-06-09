import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# The dropdown HTML structure to inject
dropdown_html = """
                <!-- Notification Dropdown -->
                <div id="notification-dropdown" class="absolute top-16 right-4 lg:right-24 w-80 bg-white rounded-2xl shadow-xl border border-slate-100 hidden z-50 flex flex-col transform transition-all scale-95 opacity-0 origin-top-right">
                    <div class="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50 rounded-t-2xl">
                        <h3 class="font-bold text-slate-800">Notifikasi</h3>
                        <span id="notif-unread-count" class="bg-blue-100 text-blue-700 text-xs px-2 py-0.5 rounded-full font-semibold hidden">0 Baru</span>
                    </div>
                    <div id="notification-list" class="max-h-80 overflow-y-auto p-2 space-y-1">
                        <!-- Notifications will be loaded here -->
                        <div class="text-center p-4 text-slate-400 text-sm">Belum ada notifikasi</div>
                    </div>
                </div>
"""

# The updated button HTML with id and badge
button_replacement = """
                <!-- Notification Button & Dropdown Container -->
                <div class="relative flex items-center">
                    <button id="btn-open-notifications" class="p-2 text-slate-600 hover:bg-slate-100 rounded-full transition-colors relative">
                        <span class="material-symbols-outlined">notifications</span>
                        <span id="notif-badge" class="absolute top-1.5 right-1.5 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-white hidden"></span>
                    </button>
                    <!-- Notification Dropdown -->
                    <div id="notification-dropdown" class="absolute top-12 right-0 w-80 bg-white rounded-2xl shadow-xl border border-slate-100 hidden z-50 flex flex-col transform transition-all scale-95 opacity-0 origin-top-right">
                        <div class="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50 rounded-t-2xl">
                            <h3 class="font-bold text-slate-800">Notifikasi</h3>
                            <span id="notif-unread-count" class="bg-blue-100 text-blue-700 text-xs px-2 py-0.5 rounded-full font-semibold hidden">0 Baru</span>
                        </div>
                        <div id="notification-list" class="max-h-80 overflow-y-auto p-2 space-y-1">
                            <div class="text-center p-4 text-slate-400 text-sm">Belum ada notifikasi</div>
                        </div>
                    </div>
                </div>
"""

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # If already injected, skip
    if 'id="notification-dropdown"' in content:
        continue

    # Try to find the notification button in index.html, riwayat.html, daftar-mobil.html etc
    # Pattern 1:
    pattern1 = re.compile(r'<button id="btn-open-notifications" class=".*?<span class="material-symbols-outlined">notifications</span>\s*</button>', re.DOTALL)
    if pattern1.search(content):
        content = pattern1.sub(button_replacement, content)
    else:
        # Pattern 2: admin.html
        pattern2 = re.compile(r'<button\s*class="[^"]*"\s*>\s*<span class="material-symbols-outlined"[^>]*>notifications</span>\s*</button>', re.DOTALL)
        if pattern2.search(content):
            content = pattern2.sub(button_replacement, content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Injected notification UI into HTML files.")
