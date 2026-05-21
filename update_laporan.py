import os
import re

files = ['manajemen-armada.html', 'manajemen-user.html', 'admin.html', 'admin-riwayat.html']
for f in files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    
    # Replace href="#" onclick="..." with href="admin-laporan.html"
    content = re.sub(r'href="#" onclick="alert\(\'Fitur Laporan segera hadir!\'\); return false;"', r'href="admin-laporan.html"', content)
    
    # For manajemen-armada and manajemen-user, Laporan href is admin-riwayat.html
    # We want to replace href="admin-riwayat.html" with href="admin-laporan.html" ONLY for the Laporan link.
    # The Laporan link has <span class="material-symbols-outlined" data-icon="assessment">assessment</span>
    # So we replace:
    # href="admin-riwayat.html">\n                <span class="material-symbols-outlined" data-icon="assessment">assessment</span>
    # with:
    # href="admin-laporan.html">\n                <span class="material-symbols-outlined" data-icon="assessment">assessment</span>
    
    content = re.sub(
        r'href="admin-riwayat\.html"([^>]*>\s*<span[^>]*>assessment</span>)',
        r'href="admin-laporan.html"\1',
        content
    )
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Updated links!")
