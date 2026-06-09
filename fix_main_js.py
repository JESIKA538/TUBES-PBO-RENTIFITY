import os
import re

file_path = 'c:\\TUBES PBO RENTIFITY\\main.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update element IDs
content = content.replace("getElementById('notif-dropdown')", "getElementById('notification-dropdown')")
content = content.replace("getElementById('notif-list')", "getElementById('notification-list')")

# 2. Add unread count UI mapping
content = content.replace("const notifBadge = document.getElementById('notif-badge');",
                          "const notifBadge = document.getElementById('notif-badge');\n    const notifUnreadCount = document.getElementById('notif-unread-count');")

# 3. Update dropdown animation logic
content = content.replace("notifDropdown.classList.remove('hidden');", "notifDropdown.classList.remove('hidden');\n                setTimeout(() => notifDropdown.classList.remove('scale-95', 'opacity-0'), 10);")
content = content.replace("notifDropdown.classList.add('hidden');", "notifDropdown.classList.add('scale-95', 'opacity-0');\n                setTimeout(() => notifDropdown.classList.add('hidden'), 200);")

# 4. Fix snake_case API mappings
content = content.replace("if (!notif.isRead) unreadCount++;", "const isRead = notif.is_read || notif.isRead;\n                    if (!isRead) unreadCount++;")
content = content.replace("notif.isRead ?", "isRead ?")
content = content.replace("if (!notif.isRead) {", "if (!isRead) {")
content = content.replace("notif.isRead = true;", "notif.isRead = true;\n                            notif.is_read = true;")
content = content.replace("notif.createdAt", "(notif.created_at || notif.createdAt)")

# 5. Update Badge to also update notif-unread-count
badge_old = """        function updateBadge(count) {
            if (count > 0) {
                notifBadge.textContent = count > 9 ? '9+' : count;
                notifBadge.classList.remove('hidden');
            } else {
                notifBadge.classList.add('hidden');
            }
        }"""

badge_new = """        function updateBadge(count) {
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
        }"""

content = content.replace(badge_old, badge_new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed main.js notification logic successfully.")
