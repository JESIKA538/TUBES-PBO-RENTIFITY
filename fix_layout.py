import os
import re

for filename in os.listdir('.'):
    if filename.endswith('.html'):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix missing lg:ml-72 on main tag if file has <aside class="fixed left-0
        if '<aside' in content and 'left-0' in content and '<main' in content:
            # We split by <main to find the main tag's attributes
            parts = content.split('<main')
            if len(parts) > 1:
                main_attrs = parts[1].split('>')[0]
                if 'lg:ml-72' not in main_attrs and 'class="' in main_attrs:
                    content = re.sub(r'(<main\s+class=")([^"]*)(")', r'\g<1>lg:ml-72 \g<2>\g<3>', content)

        # Fix remaining hardcoded avatars
        content = re.sub(r'(<img[^>]+id="nav-profile-img"[^>]+src=")([^"]*)(")', r'\g<1>jeje_profile.png\g<3>', content)
        content = re.sub(r'(<img[^>]+alt="Alex Walker"[^>]+src=")([^"]*)(")', r'\g<1>jeje_profile.png\g<3>', content)
        
        # Another pattern just in case
        content = re.sub(r'(<img[^>]*class="w-10 h-10 rounded-full[^"]*"[^>]*src=")([^"]*)(")', r'\g<1>jeje_profile.png\g<3>', content)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
print('Fixed sidebar overlap and remaining avatars.')
