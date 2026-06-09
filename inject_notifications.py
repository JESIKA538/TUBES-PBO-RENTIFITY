import os
import re

directory = r"c:\TUBES PBO RENTIFITY"
html_files = [f for f in os.listdir(directory) if f.endswith('.html')]

bell_html = """
            <!-- Notification Bell -->
            <div class="relative">
                <button id="btn-open-notifications" class="p-2 rounded-full hover:bg-surface-container-high transition-colors relative">
                    <span class="material-symbols-outlined">notifications</span>
                    <span id="notif-badge" class="absolute top-1 right-1 w-3.5 h-3.5 bg-error-red text-white rounded-full text-[9px] font-bold flex items-center justify-center border-2 border-surface hidden">0</span>
                </button>
                
                <!-- Notification Dropdown -->
                <div id="notif-dropdown" class="absolute right-0 mt-2 w-80 bg-surface dark:bg-inverse-surface border border-outline-variant/30 shadow-xl rounded-xl hidden z-[100] flex flex-col max-h-[400px]">
                    <div class="p-4 border-b border-outline-variant/30 flex justify-between items-center bg-surface-container dark:bg-inverse-surface rounded-t-xl">
                        <h4 class="font-headline-sm text-sm text-on-surface dark:text-inverse-on-surface font-bold">Notifikasi</h4>
                    </div>
                    <div id="notif-list" class="overflow-y-auto flex-1 p-2 space-y-1">
                        <div class="p-4 text-center text-sm text-on-surface-variant">Memuat notifikasi...</div>
                    </div>
                </div>
            </div>
"""

search_button_pattern = re.compile(
    r'(<button class="[^"]*">\s*<span class="material-symbols-outlined"[^>]*>search</span>\s*</button>)'
)

for filename in html_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "btn-open-notifications" not in content:
        # Insert bell_html after the search button
        new_content, count = search_button_pattern.subn(r'\1\n' + bell_html, content)
        if count > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Injected Bell into {filename}")

# Inject JS logic into main.js
main_js_path = os.path.join(directory, 'main.js')
with open(main_js_path, 'r', encoding='utf-8') as f:
    main_js = f.read()

notif_js = """
// ─────────────────────────────────────────────────────────
// 8. NOTIFICATION BELL SYNC
// ─────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    const btnOpenNotif = document.getElementById('btn-open-notifications');
    const notifDropdown = document.getElementById('notif-dropdown');
    const notifList = document.getElementById('notif-list');
    const notifBadge = document.getElementById('notif-badge');
    
    if (btnOpenNotif && notifDropdown && notifList) {
        let isNotifOpen = false;
        
        btnOpenNotif.addEventListener('click', async (e) => {
            e.stopPropagation();
            isNotifOpen = !isNotifOpen;
            if (isNotifOpen) {
                notifDropdown.classList.remove('hidden');
                await fetchAndRenderNotifications();
            } else {
                notifDropdown.classList.add('hidden');
            }
        });
        
        document.addEventListener('click', (e) => {
            if (isNotifOpen && !notifDropdown.contains(e.target) && !btnOpenNotif.contains(e.target)) {
                notifDropdown.classList.add('hidden');
                isNotifOpen = false;
            }
        });

        async function fetchAndRenderNotifications() {
            try {
                if (!window.NotificationsAPI) return; // Wait for API
                const data = await window.NotificationsAPI.getAll();
                notifList.innerHTML = '';
                
                if (!data || data.length === 0) {
                    notifList.innerHTML = '<div class="p-4 text-center text-sm text-on-surface-variant">Belum ada notifikasi</div>';
                    updateBadge(0);
                    return;
                }
                
                let unreadCount = 0;
                
                data.forEach(notif => {
                    if (!notif.isRead) unreadCount++;
                    
                    const item = document.createElement('div');
                    item.className = `p-3 rounded-lg text-sm border-b border-outline-variant/20 last:border-0 cursor-pointer hover:bg-surface-container transition-colors ${notif.isRead ? 'opacity-70' : 'bg-primary-container/20 dark:bg-primary-container/10 font-medium'}`;
                    item.innerHTML = `
                        <div class="flex gap-3 items-start">
                            <span class="material-symbols-outlined text-primary text-xl mt-0.5">info</span>
                            <div class="flex-1">
                                <p class="text-on-surface dark:text-inverse-on-surface">${notif.message}</p>
                                <span class="text-[10px] text-on-surface-variant mt-1 block">${new Date(notif.createdAt).toLocaleString()}</span>
                            </div>
                        </div>
                    `;
                    
                    item.addEventListener('click', async () => {
                        if (!notif.isRead) {
                            await window.NotificationsAPI.markAsRead(notif.id);
                            item.classList.remove('bg-primary-container/20', 'dark:bg-primary-container/10', 'font-medium');
                            item.classList.add('opacity-70');
                            notif.isRead = true;
                            unreadCount--;
                            updateBadge(unreadCount);
                        }
                    });
                    
                    notifList.appendChild(item);
                });
                
                updateBadge(unreadCount);
            } catch (err) {
                notifList.innerHTML = '<div class="p-4 text-center text-sm text-error">Gagal memuat notifikasi</div>';
            }
        }
        
        function updateBadge(count) {
            if (count > 0) {
                notifBadge.textContent = count > 9 ? '9+' : count;
                notifBadge.classList.remove('hidden');
            } else {
                notifBadge.classList.add('hidden');
            }
        }

        // Fetch unread count on initial load
        if (window.NotificationsAPI) {
            window.NotificationsAPI.getAll().then(data => {
                if (data) {
                    const unread = data.filter(n => !n.isRead).length;
                    updateBadge(unread);
                }
            }).catch(e => {});
        }
    }
});
"""

if "NOTIFICATION BELL SYNC" not in main_js:
    with open(main_js_path, 'a', encoding='utf-8') as f:
        f.write(notif_js)
    print("Injected JS into main.js")
