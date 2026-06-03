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
        
        // Aturan khusus pencocokan untuk riwayat.html / admin-riwayat.html
        if (currentPath === 'riwayat.html') {
            const iconSpan = link.querySelector('.material-symbols-outlined');
            const iconName = iconSpan ? (iconSpan.getAttribute('data-icon') || iconSpan.textContent.trim()) : '';
            
            if (isAdmin) {
                // Admin di riwayat.html -> menu Laporan yang aktif
                isActive = (href === 'riwayat.html' || href === 'admin-laporan.html') && iconName === 'assessment';
            } else {
                // Customer di riwayat.html -> menu Riwayat Pembayaran yang aktif
                isActive = href === 'riwayat.html' && iconName === 'payments';
            }
        } else {
            // Pencocokan umum berdasarkan nama berkas href
            isActive = href === currentPath;
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
