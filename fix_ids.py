import os

# 1. Fix main.js
main_path = 'c:\\TUBES PBO RENTIFITY\\main.js'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("getElementById('notification-dropdown')", "getElementById('notif-dropdown')")
content = content.replace("getElementById('notification-list')", "getElementById('notif-list')")

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Fix HTML files
html_files = [f for f in os.listdir('.') if f.endswith('.html')]
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'notification-dropdown' in content:
        content = content.replace('notification-dropdown', 'notif-dropdown')
        content = content.replace('notification-list', 'notif-list')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Standardized IDs to notif-dropdown and notif-list.")
