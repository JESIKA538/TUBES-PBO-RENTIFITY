document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle
    const menuButtons = document.querySelectorAll('[data-icon="menu"]');
    const sidebar = document.querySelector('aside');

    if (sidebar) {
        menuButtons.forEach(btn => {
            const clickable = btn.closest('button') || btn;
            clickable.style.cursor = 'pointer';

            clickable.addEventListener('click', () => {
                sidebar.classList.toggle('hidden');
                sidebar.classList.toggle('flex');

                if (!document.getElementById('sidebar-overlay') && !sidebar.classList.contains('hidden')) {
                    const overlay = document.createElement('div');
                    overlay.id = 'sidebar-overlay';
                    overlay.className = 'fixed inset-0 bg-black/50 z-30 lg:hidden';
                    overlay.addEventListener('click', () => {
                        sidebar.classList.add('hidden');
                        sidebar.classList.remove('flex');
                        overlay.remove();
                    });
                    document.body.appendChild(overlay);
                } else if (document.getElementById('sidebar-overlay') && sidebar.classList.contains('hidden')) {
                    document.getElementById('sidebar-overlay').remove();
                }
            });
        });
    }

    // 2. Favorite / Action Icons Toggle
    const favoriteIcons = document.querySelectorAll('[data-icon="favorite"]');
    favoriteIcons.forEach(icon => {
        const btn = icon.closest('button') || icon;
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const isFilled = icon.style.fontVariationSettings.includes("'FILL' 1");
            if (isFilled) {
                icon.style.fontVariationSettings = "'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24";
                icon.classList.remove('text-error-red');
            } else {
                icon.style.fontVariationSettings = "'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24";
                icon.classList.add('text-error-red');
            }
        });
    });

    // 3. Bottom navigation micro-animation
    const bottomNavLinks = document.querySelectorAll('nav.fixed.bottom-0 a');
    bottomNavLinks.forEach(link => {
        link.addEventListener('click', function () {
            const icon = this.querySelector('.material-symbols-outlined');
            if (icon) {
                icon.style.transform = 'scale(0.9)';
                setTimeout(() => { icon.style.transform = 'scale(1)'; }, 150);
            }
        });
    });

    // ─────────────────────────────────────────────────────────
    // 4. GLOBAL THEME SYNC
    //    Otomatis terapkan tema (gelap/terang) sesuai localStorage
    // ─────────────────────────────────────────────────────────
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'dark') {
        document.documentElement.classList.add('dark');
        document.documentElement.classList.remove('light');
    } else {
        document.documentElement.classList.add('light');
        document.documentElement.classList.remove('dark');
    }

    // ─────────────────────────────────────────────────────────
    // 5. GLOBAL PROFILE SYNC
    //    Otomatis sinkronkan foto/nama user di semua halaman
    //    langsung dari localStorage — instan, tanpa request API.
    // ─────────────────────────────────────────────────────────
        syncUserProfile();
    adjustNavigationForRole();

    // ─────────────────────────────────────────────────────────
    // 6. GLOBAL SIDEBAR ACTIVE TAB SYNC
    //    Otomatis set tab aktif pada sidebar berdasarkan URL
    // ─────────────────────────────────────────────────────────
    syncActiveSidebarTab();
    initGlobalSupportModal();
});

/**
 * Buat avatar inisial dari nama user (canvas → data URL).
 * Dipakai ketika user belum upload foto profil.
 * Warna unik/deterministik berdasarkan email user.
 */
function generateInitialsAvatar(name, email) {
    const canvas = document.createElement('canvas');
    canvas.width = 100;
    canvas.height = 100;
    const ctx = canvas.getContext('2d');

    // Warna unik dari email/nama
    const seed = email || name || 'user';
    let hash = 0;
    for (let i = 0; i < seed.length; i++) {
        hash = seed.charCodeAt(i) + ((hash << 5) - hash);
    }
    const hue = Math.abs(hash) % 360;

    // Background lingkaran berwarna
    ctx.fillStyle = `hsl(${hue}, 55%, 38%)`;
    ctx.beginPath();
    ctx.arc(50, 50, 50, 0, Math.PI * 2);
    ctx.fill();

    // Teks inisial
    const initials = (name || 'U')
        .split(' ')
        .map(w => w[0])
        .join('')
        .substring(0, 2)
        .toUpperCase();

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 36px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(initials, 50, 52);

    return canvas.toDataURL('image/png');
}

/**
 * Sinkronkan semua elemen profil di halaman aktif
 * berdasarkan data user di localStorage.
 * Dipanggil otomatis dari DOMContentLoaded di setiap halaman.
 */
function syncUserProfile() {
    const userStr = localStorage.getItem('rentify_user');
    if (!userStr) return;

    let user;
    try { user = JSON.parse(userStr); } catch (e) { return; }

    const name       = user.name       || 'Pengguna';
    const email      = user.email      || '';
    const occupation = user.occupation || 'Pelanggan Rentify';
    const isAdmin    = user.role === 'admin';

    // Gunakan avatar tersimpan, atau generate dari inisial nama
    const avatarSrc = (user.avatar && user.avatar.startsWith('data:'))
        ? user.avatar
        : (user.avatar
            ? user.avatar
            : generateInitialsAvatar(name, email));

    // ── Update semua elemen foto profil ──
    const imgIds = ['nav-profile-img', 'nav-profile-img-top', 'aside-profile-img', 'form-profile-img'];
    imgIds.forEach(id => {
        const el = document.getElementById(id);
        if (el && el.tagName === 'IMG') {
            el.src = avatarSrc;
            el.alt = name;
        }
    });

    // ── Update semua elemen nama ──
    const nameIds = ['profile-name-aside', 'aside-profile-name'];
    nameIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.textContent = name;
    });

    // ── Update semua elemen jabatan/role ──
    const roleIds = ['profile-occupation-aside', 'aside-profile-role'];
    roleIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.textContent = isAdmin ? 'Administrator' : occupation;
    });
}

/**
 * Otomatis deteksi halaman aktif dan aktifkan tab menu yang sesuai
 * di sidebar, serta hapus style aktif dari menu lainnya.
 */
function syncActiveSidebarTab() {
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('aside nav a, aside div.px-4.py-6 a, aside div.px-6.mb-8 a');
    if (navLinks.length === 0) return;

    const userStr = localStorage.getItem('rentify_user');
    let user = null;
    if (userStr) {
        try { user = JSON.parse(userStr); } catch (e) {}
    }
    const isAdmin = user && user.role === 'admin';

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (!href) return;

        let isActive = false;
        const hrefFilename = href.split('/').pop();
        
        // Aturan khusus pencocokan untuk riwayat.html / admin-riwayat.html
        if (currentPath === 'riwayat.html') {
            const iconSpan = link.querySelector('.material-symbols-outlined');
            const iconName = iconSpan ? (iconSpan.getAttribute('data-icon') || iconSpan.textContent.trim()) : '';
            
            if (isAdmin) {
                // Admin di riwayat.html -> menu Laporan yang aktif
                isActive = (hrefFilename === 'riwayat.html' || hrefFilename === 'admin-laporan.html') && iconName === 'assessment';
            } else {
                // Customer di riwayat.html -> menu Riwayat Pembayaran yang aktif
                isActive = hrefFilename === 'riwayat.html' && iconName === 'payments';
            }
        } else {
            // Pencocokan umum berdasarkan nama berkas href
            isActive = hrefFilename === currentPath;
        }

        // Daftar class Tailwind untuk status Aktif dan Tidak Aktif
        const activeClasses = ['bg-secondary-container', 'dark:bg-secondary', 'text-on-secondary-container', 'dark:text-on-secondary', 'font-bold'];
        const inactiveClasses = ['text-on-surface-variant', 'dark:text-surface-variant', 'hover:bg-surface-container-high'];

        const iconSpan = link.querySelector('.material-symbols-outlined');
        const textSpan = link.querySelector('span:not(.material-symbols-outlined)');

        if (isActive) {
            link.classList.add(...activeClasses);
            link.classList.remove(...inactiveClasses);
            if (iconSpan) {
                iconSpan.style.fontVariationSettings = "'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24";
            }
            if (textSpan) {
                textSpan.classList.add('font-bold');
            }
        } else {
            // Hindari menghapus style dari tombol Keluar (logout)
            if (!link.classList.contains('text-error-red') && !link.id.includes('logout')) {
                link.classList.remove(...activeClasses);
                link.classList.add(...inactiveClasses);
                if (iconSpan) {
                    iconSpan.style.fontVariationSettings = "'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24";
                }
                if (textSpan) {
                    textSpan.classList.remove('font-bold');
                }
            }
        }
    });
}

/**
 * Otomatis sinkronkan label menu di sidebar ke Bahasa Indonesia
 * dan sembunyikan link menu yang tidak relevan dengan peran (role) pengguna.
 * Menghindari ketidak-konsistenan bahasa dan akses menu antar role.
 */
function adjustNavigationForRole() {
    try {
        const userStr = localStorage.getItem('rentify_user');
        if (!userStr) return;

        let user;
        try { user = JSON.parse(userStr); } catch (e) { return; }

        const isAdmin = user.role === 'admin';

        // 1. Sesuaikan link & label sidebar (Desktop)
        const sidebarLinks = document.querySelectorAll('aside a, #sidebar-nav a');
        sidebarLinks.forEach(link => {
            try {
                const iconSpan = link.querySelector('.material-symbols-outlined');
                if (iconSpan) {
                    const iconName = iconSpan.getAttribute('data-icon') || iconSpan.textContent.trim();
                    
                    // Sembunyikan menu tidak relevan
                    if (isAdmin) {
                        // Admin: sembunyikan "Riwayat Pembayaran" (payments)
                        if (iconName === 'payments') {
                            link.style.display = 'none';
                        }
                    } else {
                        // Customer: sembunyikan "Laporan" (assessment) dan "Manajemen Pengguna" (group)
                        if (iconName === 'assessment' || iconName === 'group') {
                            link.style.display = 'none';
                        }
                    }

                    // Ubah ke Bahasa Indonesia secara konsisten
                    if (!link.classList.contains('text-error-red') && !link.id.includes('logout')) {
                        let textElement = link.querySelector('span:not(.material-symbols-outlined)');
                        if (textElement) {
                            if (iconName === 'dashboard') textElement.textContent = 'Dasbor';
                            else if (iconName === 'directions_car') textElement.textContent = 'Armada Mobil';
                            else if (iconName === 'calendar_today') textElement.textContent = 'Pesanan Saya';
                            else if (iconName === 'settings') textElement.textContent = 'Pengaturan';
                            else if (iconName === 'group') textElement.textContent = 'Manajemen Pengguna';
                            else if (iconName === 'payments') textElement.textContent = 'Riwayat Pembayaran';
                            else if (iconName === 'assessment') textElement.textContent = 'Laporan';
                        } else {
                            let textNode = null;
                            link.childNodes.forEach(node => {
                                if (node.nodeType === 3 && node.textContent.trim() !== '') {
                                    textNode = node;
                                }
                            });
                            if (textNode) {
                                if (iconName === 'dashboard') textNode.textContent = ' Dasbor';
                                else if (iconName === 'directions_car') textNode.textContent = ' Armada Mobil';
                                else if (iconName === 'calendar_today') textNode.textContent = ' Pesanan Saya';
                                else if (iconName === 'settings') textNode.textContent = ' Pengaturan';
                                else if (iconName === 'group') textNode.textContent = ' Manajemen Pengguna';
                                else if (iconName === 'payments') textNode.textContent = ' Riwayat Pembayaran';
                                else if (iconName === 'assessment') textNode.textContent = ' Laporan';
                            }
                        }
                    }
                }
            } catch (errInner) {
                console.error("Error processing sidebar link:", errInner);
            }
        });

        // 2. Sesuaikan bottom navigation (Mobile)
        const bottomNav = document.querySelector('nav.fixed');
        if (bottomNav) {
            const bottomNavLinks = bottomNav.querySelectorAll('a');
            bottomNavLinks.forEach(link => {
                try {
                    const iconSpan = link.querySelector('.material-symbols-outlined');
                    if (iconSpan) {
                        const iconName = iconSpan.getAttribute('data-icon') || iconSpan.textContent.trim();
                        const textSpan = link.querySelector('span:not(.material-symbols-outlined)');
                        
                        if (!isAdmin) {
                            // Customer mobile bottom nav: ganti Laporan (assessment) dengan Riwayat (payments)
                            if (iconName === 'assessment') {
                                iconSpan.textContent = 'payments';
                                iconSpan.setAttribute('data-icon', 'payments');
                                if (textSpan) {
                                    textSpan.textContent = 'Riwayat';
                                }
                            }
                        } else {
                            // Admin mobile bottom nav: ganti Riwayat (payments) dengan Laporan (assessment)
                            if (iconName === 'payments') {
                                iconSpan.textContent = 'assessment';
                                iconSpan.setAttribute('data-icon', 'assessment');
                                if (textSpan) {
                                    textSpan.textContent = 'Laporan';
                                }
                            }
                        }
                    }
                } catch (errInnerNav) {
                    console.error("Error processing bottom nav link:", errInnerNav);
                }
            });
        }
    } catch (errOuter) {
        console.error("Error in adjustNavigationForRole:", errOuter);
    }
}

/**
 * Inisialisasi Modal Dukungan Pelanggan (Concierge Support 24/7) secara global.
 * Membuat elemen modal secara dinamis dan menempelkannya ke body,
 * lalu menghubungkan semua tombol/link dukungan di halaman.
 */
function initGlobalSupportModal() {
    // 1. Cek jika modal sudah ada
    if (document.getElementById('global-support-modal')) return;

    // 2. Buat elemen modal HTML
    const modalContainer = document.createElement('div');
    modalContainer.id = 'global-support-modal';
    modalContainer.className = 'fixed inset-0 z-[100] hidden items-center justify-center bg-black/60 backdrop-blur-sm transition-all duration-300 opacity-0';
    
    modalContainer.innerHTML = `
        <div class="bg-white dark:bg-zinc-900 rounded-2xl p-6 max-w-sm w-full mx-4 shadow-2xl transform scale-95 transition-all duration-300 border border-outline-variant/30 flex flex-col gap-5 text-left">
            <div class="flex justify-between items-center">
                <h3 class="font-headline-sm text-headline-sm text-zinc-900 dark:text-white font-bold flex items-center gap-2">
                    <span class="material-symbols-outlined text-secondary" style="font-variation-settings: 'FILL' 1">support_agent</span>
                    Dukungan Concierge
                </h3>
                <button id="close-support-modal" class="text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 p-1.5 rounded-full hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                    <span class="material-symbols-outlined text-[20px]">close</span>
                </button>
            </div>
            
            <p class="text-body-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
                Layanan concierge 24/7 kami siap membantu segala kebutuhan sewa, konfirmasi pembayaran, hingga bantuan darurat di jalan.
            </p>
            
            <div class="flex flex-col gap-3">
                <!-- WhatsApp Option -->
                <a href="https://wa.me/6281234567890?text=Halo%20Rentify%20Concierge,%20saya%20butuh%20bantuan%20terkait%20layanan%20sewa%20mobil." target="_blank" class="flex items-center gap-4 p-3 rounded-xl bg-emerald-50 hover:bg-emerald-100 dark:bg-emerald-950/20 dark:hover:bg-emerald-950/40 transition-colors border border-emerald-500/20 group">
                    <div class="w-10 h-10 rounded-full bg-emerald-500 flex items-center justify-center text-white shadow-sm flex-shrink-0">
                        <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1">chat</span>
                    </div>
                    <div class="flex-grow min-w-0">
                        <p class="font-bold text-xs text-emerald-950 dark:text-emerald-300">WhatsApp Concierge</p>
                        <p class="text-[10px] text-emerald-600 dark:text-emerald-400/80 truncate">Respon instan • 24 Jam Aktif</p>
                    </div>
                    <span class="material-symbols-outlined text-emerald-500 group-hover:translate-x-1 transition-transform flex-shrink-0">arrow_forward</span>
                </a>
                
                <!-- Hotline Call Option -->
                <a href="tel:+6221500888" class="flex items-center gap-4 p-3 rounded-xl bg-blue-50 hover:bg-blue-100 dark:bg-blue-950/20 dark:hover:bg-blue-950/40 transition-colors border border-blue-500/20 group">
                    <div class="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white shadow-sm flex-shrink-0">
                        <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1">call</span>
                    </div>
                    <div class="flex-grow min-w-0">
                        <p class="font-bold text-xs text-blue-950 dark:text-blue-300">Hotline Panggilan Darurat</p>
                        <p class="text-[10px] text-blue-600 dark:text-blue-400/80 truncate">+62 21 500 888</p>
                    </div>
                    <span class="material-symbols-outlined text-blue-500 group-hover:translate-x-1 transition-transform flex-shrink-0">arrow_forward</span>
                </a>
                
                <!-- Email Option -->
                <a href="mailto:support@rentify.id?subject=Bantuan%20Pelanggan%20Rentify" class="flex items-center gap-4 p-3 rounded-xl bg-zinc-50 hover:bg-zinc-100 dark:bg-zinc-800/40 dark:hover:bg-zinc-800/70 transition-colors border border-outline-variant/30 group">
                    <div class="w-10 h-10 rounded-full bg-zinc-500 flex items-center justify-center text-white shadow-sm flex-shrink-0">
                        <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1">mail</span>
                    </div>
                    <div class="flex-grow min-w-0">
                        <p class="font-bold text-xs text-zinc-800 dark:text-zinc-200">Email Hubungan Pelanggan</p>
                        <p class="text-[10px] text-zinc-500 dark:text-zinc-400 truncate">support@rentify.id</p>
                    </div>
                    <span class="material-symbols-outlined text-zinc-400 group-hover:translate-x-1 transition-transform flex-shrink-0">arrow_forward</span>
                </a>
            </div>
        </div>
    `;

    document.body.appendChild(modalContainer);

    // 3. Fungsi Buka & Tutup Modal dengan animasi
    function openModal() {
        modalContainer.classList.remove('hidden');
        modalContainer.classList.add('flex');
        // Trigger reflow untuk animasi transition
        setTimeout(() => {
            modalContainer.classList.remove('opacity-0');
            modalContainer.classList.add('opacity-100');
            modalContainer.querySelector('div').classList.remove('scale-95');
            modalContainer.querySelector('div').classList.add('scale-100');
        }, 10);
    }

    function closeModal() {
        modalContainer.classList.remove('opacity-100');
        modalContainer.classList.add('opacity-0');
        modalContainer.querySelector('div').classList.remove('scale-100');
        modalContainer.querySelector('div').classList.add('scale-95');
        setTimeout(() => {
            modalContainer.classList.remove('flex');
            modalContainer.classList.add('hidden');
        }, 300);
    }

    // Bind event penutup modal
    const closeBtn = modalContainer.querySelector('#close-support-modal');
    closeBtn.addEventListener('click', closeModal);

    // Klik di area luar modal untuk menutup
    modalContainer.addEventListener('click', (e) => {
        if (e.target === modalContainer) closeModal();
    });

    // 4. Cari dan hubungkan semua tombol/link bertuliskan "Hubungi Dukungan" atau "Hubungi Agen"
    function bindSupportButtons() {
        const elements = document.querySelectorAll('button, a, div');
        elements.forEach(el => {
            if (el.tagName === 'BUTTON' || el.tagName === 'A' || el.classList.contains('cursor-pointer')) {
                const text = el.textContent.replace(/\s+/g, ' ').trim().toLowerCase();
                if (text.includes('hubungi dukungan') || text.includes('hubungi agen') || text.includes('contact support')) {
                    // Cek jika listener sudah dipasang (menggunakan dataset flag untuk menghindari multiple listener)
                    if (el.dataset.supportBound) return;
                    el.dataset.supportBound = "true";

                    el.addEventListener('click', (e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        openModal();
                    });
                    el.style.cursor = 'pointer';
                }
            }
        });
    }

    // Jalankan binding awal
    bindSupportButtons();

    // Jalankan ulang binding jika ada penambahan elemen dinamis
    const observer = new MutationObserver(bindSupportButtons);
    observer.observe(document.body, { childList: true, subtree: true });
}

// ─────────────────────────────────────────────────────────
// 7. GLOBAL LANGUAGE SYNC (Terjemahan Sederhana)
// ─────────────────────────────────────────────────────────
const translations = {
    'en': {
        'Dashboard': 'Dashboard',
        'Dasbor': 'Dashboard',
        'Armada Mobil': 'Car Fleet',
        'Mobil': 'Cars',
        'Pesanan Saya': 'My Bookings',
        'Pesanan': 'Bookings',
        'Riwayat Pembayaran': 'Payment History',
        'Riwayat': 'History',
        'Laporan': 'Reports',
        'Pengaturan': 'Settings',
        'Keluar': 'Logout',
        'Profil': 'Profile',
        'Beranda': 'Home',
        'Selamat datang kembali': 'Welcome back'
    }
};

function applyLanguage() {
    const lang = localStorage.getItem('rentify_lang') || 'id';
    if (lang === 'id') return; // Default is Indonesian
    
    const dict = translations[lang];
    if (!dict) return;

    // Translate common texts
    const elementsToTranslate = document.querySelectorAll('span, a, h1, h2, h3, h4, button');
    elementsToTranslate.forEach(el => {
        // Only translate if element has direct text node (not nested HTML like icons)
        if (el.childNodes.length === 1 && el.childNodes[0].nodeType === 3) {
            const originalText = el.textContent.trim();
            for (const [idText, enText] of Object.entries(dict)) {
                if (originalText === idText || originalText.includes(idText + ',')) {
                    el.textContent = el.textContent.replace(idText, enText);
                }
            }
        } else {
            // For elements with icons + text
            el.childNodes.forEach(node => {
                if (node.nodeType === 3 && node.textContent.trim() !== '') {
                    const originalText = node.textContent.trim();
                    for (const [idText, enText] of Object.entries(dict)) {
                        if (originalText === idText || originalText.includes(idText + ',')) {
                            node.textContent = node.textContent.replace(idText, enText);
                        }
                    }
                }
            });
        }
    });
}

// Call applyLanguage on load
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(applyLanguage, 100); // slight delay to let other DOM scripts finish
});

// ─────────────────────────────────────────────────────────
// 8. NOTIFICATION BELL SYNC
// ─────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    const btnOpenNotif = document.getElementById('btn-open-notifications');
    const notifDropdown = document.getElementById('notif-dropdown');
    const notifList = document.getElementById('notif-list');
    const notifBadge = document.getElementById('notif-badge');
    const notifUnreadCount = document.getElementById('notif-unread-count');
    
    if (btnOpenNotif && notifDropdown && notifList) {
        let isNotifOpen = false;
        
        btnOpenNotif.addEventListener('click', async (e) => {
            e.stopPropagation();
            isNotifOpen = !isNotifOpen;
            if (isNotifOpen) {
                notifDropdown.classList.remove('hidden');
                setTimeout(() => notifDropdown.classList.remove('scale-95', 'opacity-0'), 10);
                await fetchAndRenderNotifications();
            } else {
                notifDropdown.classList.add('scale-95', 'opacity-0');
                setTimeout(() => notifDropdown.classList.add('hidden'), 200);
            }
        });
        
        document.addEventListener('click', (e) => {
            if (isNotifOpen && !notifDropdown.contains(e.target) && !btnOpenNotif.contains(e.target)) {
                notifDropdown.classList.add('scale-95', 'opacity-0');
                setTimeout(() => notifDropdown.classList.add('hidden'), 200);
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
                    const isRead = notif.is_read || notif.isRead;
                    if (!isRead) unreadCount++;
                    
                    const item = document.createElement('div');
                    item.className = `p-3 rounded-lg text-sm border-b border-outline-variant/20 last:border-0 cursor-pointer hover:bg-surface-container transition-colors ${isRead ? 'opacity-70' : 'bg-primary-container/20 dark:bg-primary-container/10 font-medium'}`;
                    item.innerHTML = `
                        <div class="flex gap-3 items-start">
                            <span class="material-symbols-outlined text-primary text-xl mt-0.5">info</span>
                            <div class="flex-1">
                                <p class="text-on-surface dark:text-inverse-on-surface">${notif.message}</p>
                                <span class="text-[10px] text-on-surface-variant mt-1 block">${new Date((notif.created_at || notif.createdAt)).toLocaleString()}</span>
                            </div>
                        </div>
                    `;
                    
                    item.addEventListener('click', async () => {
                        if (!isRead) {
                            await window.NotificationsAPI.markAsRead(notif.id);
                            item.classList.remove('bg-primary-container/20', 'dark:bg-primary-container/10', 'font-medium');
                            item.classList.add('opacity-70');
                            notif.isRead = true;
                            notif.is_read = true;
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
                if (notifBadge) {
                    notifBadge.textContent = '';
                    notifBadge.classList.remove('hidden');
                }
                if (notifUnreadCount) {
                    notifUnreadCount.textContent = count > 9 ? '9+ Baru' : count + ' Baru';
                    notifUnreadCount.classList.remove('hidden');
                }
            } else {
                if (notifBadge) notifBadge.classList.add('hidden');
                if (notifUnreadCount) notifUnreadCount.classList.add('hidden');
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
