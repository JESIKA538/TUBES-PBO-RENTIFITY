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
    // 4. GLOBAL PROFILE SYNC
    //    Otomatis sinkronkan foto/nama user di semua halaman
    //    langsung dari localStorage — instan, tanpa request API.
    // ─────────────────────────────────────────────────────────
    syncUserProfile();
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
