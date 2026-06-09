import os
import re

directory = r"c:\TUBES PBO RENTIFITY"
html_files = [f for f in os.listdir(directory) if f.endswith('.html')]

# 1. Update HTML bodies to support dark mode
for filename in html_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the body tag and ensure it has dark mode classes
    body_pattern = r'<body class="([^"]*)"'
    
    def add_dark_classes(match):
        classes = match.group(1)
        if 'dark:bg-inverse-surface' not in classes:
            classes += ' dark:bg-inverse-surface dark:text-inverse-on-surface'
        return f'<body class="{classes}"'
    
    new_content = re.sub(body_pattern, add_dark_classes, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

print(f"Updated body tags for Dark Mode in {len(html_files)} HTML files.")

# 2. Add translation logic to main.js
main_js_path = os.path.join(directory, 'main.js')
with open(main_js_path, 'r', encoding='utf-8') as f:
    main_js = f.read()

translation_logic = """
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
"""

if "GLOBAL LANGUAGE SYNC" not in main_js:
    with open(main_js_path, 'a', encoding='utf-8') as f:
        f.write(translation_logic)
    print("Added translation logic to main.js")
else:
    print("Translation logic already exists in main.js")
