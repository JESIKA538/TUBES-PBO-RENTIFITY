document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle
    const menuButtons = document.querySelectorAll('[data-icon="menu"]');
    const sidebar = document.querySelector('aside');

    if (sidebar) {
        menuButtons.forEach(btn => {
            // Find the closest button element, or use the span itself if it's not in a button
            const clickable = btn.closest('button') || btn;
            clickable.style.cursor = 'pointer';

            clickable.addEventListener('click', () => {
                sidebar.classList.toggle('hidden');
                sidebar.classList.toggle('flex');

                // Add overlay if it doesn't exist and sidebar is open
                if (!document.getElementById('sidebar-overlay') && !sidebar.classList.contains('hidden')) {
                    const overlay = document.createElement('div');
                    overlay.id = 'sidebar-overlay';
                    overlay.className = 'fixed inset-0 bg-black/50 z-30 lg:hidden';

                    // Close sidebar when overlay is clicked
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

    // 2. Favorite / Action Icons Toggle (e.g. Heart Icon)
    // Find buttons that contain an icon with data-icon="favorite"
    const favoriteIcons = document.querySelectorAll('[data-icon="favorite"]');
    favoriteIcons.forEach(icon => {
        const btn = icon.closest('button') || icon;
        btn.addEventListener('click', function (e) {
            e.preventDefault(); // In case it's inside a form or link

            // Check if currently filled
            const isFilled = icon.style.fontVariationSettings.includes("'FILL' 1");

            if (isFilled) {
                // Remove fill, switch back to normal color
                icon.style.fontVariationSettings = "'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24";
                icon.classList.remove('text-error-red');
            } else {
                // Add fill, switch to red color
                icon.style.fontVariationSettings = "'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24";
                icon.classList.add('text-error-red');
            }
        });
    });

    // 3. Make the bottom navigation active states visually interactive
    const bottomNavLinks = document.querySelectorAll('nav.fixed.bottom-0 a');
    bottomNavLinks.forEach(link => {
        link.addEventListener('click', function () {
            // We don't prevent default so it actually navigates, 
            // but we can add a quick visual pop before navigation
            const icon = this.querySelector('.material-symbols-outlined');
            if (icon) {
                icon.style.transform = 'scale(0.9)';
                setTimeout(() => {
                    icon.style.transform = 'scale(1)';
                }, 150);
            }
        });
    });
});
