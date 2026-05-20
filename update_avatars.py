import os
import re

dir_path = r'c:\TUBES PBO RENTIFITY'

for filename in os.listdir(dir_path):
    if filename.endswith('.html'):
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace user avatar URLs
        content = re.sub(r'(<img[^>]*class="[^"]*w-10 h-10 rounded-full[^"]*"[^>]*src=")([^"]*)("[^>]*>)', r'\g<1>jeje_profile.png\g<3>', content)

        # Also fix any dynamic avatar updates that might break it if user.avatar is undefined
        content = content.replace("document.getElementById('top-bar-avatar').src = user.avatar;", "if(user.avatar) document.getElementById('top-bar-avatar').src = user.avatar;")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print('Updated avatars in all pages.')
