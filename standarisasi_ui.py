import re
import os

base_dir = r"c:\TUBES PBO RENTIFITY\views\user"
daftar_mobil = os.path.join(base_dir, "daftar-mobil.html")

with open(daftar_mobil, "r", encoding="utf-8") as f:
    content = f.read()

# Extract header
header_match = re.search(r'(<!-- TopAppBar -->.*?)</header>', content, re.DOTALL)
standard_header = header_match.group(1) + "</header>"

# Extract aside
aside_match = re.search(r'(<!-- Sidebar Navigation -->\s*<aside.*?</aside>)', content, re.DOTALL)
standard_aside = aside_match.group(1)

# Extract bottom nav
nav_match = re.search(r'(<!-- BottomNavBar \(Mobile Only\) -->\s*<nav.*?</nav>)', content, re.DOTALL)
standard_nav = nav_match.group(1)

def set_active_menu(aside_html, url_path):
    # reset all to inactive
    inactive_cls = "text-on-surface-variant dark:text-surface-variant mx-2 my-1 px-4 py-3 flex items-center gap-3 hover:bg-surface-container-high rounded-lg transition-all"
    active_cls = "bg-secondary-container dark:bg-secondary text-on-secondary-container dark:text-on-secondary rounded-lg mx-2 my-1 px-4 py-3 flex items-center gap-3 active:scale-[0.99] transition-transform duration-150"
    
    # regex to find all <a> tags in nav
    nav_inner = re.search(r'(<nav class="flex-1 flex flex-col gap-1 px-2">.*?</nav>)', aside_html, re.DOTALL).group(1)
    
    # replace all active_cls with inactive_cls
    nav_inner_reset = nav_inner.replace(active_cls, inactive_cls)
    # remove FILL 1 from all icons
    nav_inner_reset = re.sub(r' style="font-variation-settings:\s*\'FILL\'\s*1;?"', '', nav_inner_reset)
    
    # find the specific a tag and make it active
    # We will use string manipulation
    links = re.findall(r'<a.*?href="([^"]+)".*?</a>', nav_inner_reset, re.DOTALL)
    
    for link in links:
        if url_path in link:
            # Found the link, replace its class
            # Extract the whole tag
            tag_match = re.search(rf'<a[^>]*href="{re.escape(link)}"[^>]*>.*?</a>', nav_inner_reset, re.DOTALL)
            if tag_match:
                tag = tag_match.group(0)
                new_tag = tag.replace(inactive_cls, active_cls)
                # add FILL 1 to icon
                new_tag = re.sub(r'(<span class="material-symbols-outlined"[^>]*)>', r'\1 style="font-variation-settings: \'FILL\' 1;">', new_tag)
                nav_inner_reset = nav_inner_reset.replace(tag, new_tag)
                
    new_aside = aside_html.replace(nav_inner, nav_inner_reset)
    return new_aside

def set_active_bottom_nav(nav_html, url_path):
    inactive_cls = "flex flex-col items-center justify-center text-on-surface-variant dark:text-surface-variant active:bg-surface-container-high transition-colors"
    active_cls = "flex flex-col items-center justify-center text-secondary dark:text-secondary-fixed font-bold active:scale-95 duration-100"
    
    nav_html_reset = nav_html.replace(active_cls, inactive_cls)
    nav_html_reset = re.sub(r' style="font-variation-settings:\s*\'FILL\'\s*1;?"', '', nav_html_reset)
    
    links = re.findall(r'<a.*?href="([^"]+)".*?</a>', nav_html_reset, re.DOTALL)
    for link in links:
        if url_path in link:
            tag_match = re.search(rf'<a[^>]*href="{re.escape(link)}"[^>]*>.*?</a>', nav_html_reset, re.DOTALL)
            if tag_match:
                tag = tag_match.group(0)
                new_tag = tag.replace(inactive_cls, active_cls)
                new_tag = re.sub(r'(<span class="material-symbols-outlined"[^>]*)>', r'\1 style="font-variation-settings: \'FILL\' 1;">', new_tag)
                nav_html_reset = nav_html_reset.replace(tag, new_tag)
                
    return nav_html_reset


# 1. Update booking-mobil.html
booking_file = os.path.join(base_dir, "booking-mobil.html")
with open(booking_file, "r", encoding="utf-8") as f:
    b_content = f.read()

# Replace header
b_content = re.sub(r'<!-- TopAppBar -->.*?</header>', standard_header, b_content, flags=re.DOTALL)
# Wrap main content
if '<div class="flex min-h-[calc(100vh-64px)]">' not in b_content:
    b_content = re.sub(r'(<main[^>]*>)', r'<div class="flex min-h-[calc(100vh-64px)]">\n    <!-- Sidebar placeholder -->\n    \1', b_content, count=1)
    b_content = re.sub(r'(</main>)', r'\1\n    </div>', b_content)

# Update main classes
b_content = re.sub(r'<main[^>]*>', r'<main class="flex-1 lg:ml-72 pb-24 lg:pb-12 max-w-[1440px] mx-auto px-margin-mobile md:px-margin-desktop pt-8">', b_content)

# Remove old aside and nav
b_content = re.sub(r'<!-- Sidebar Navigation -->.*?</aside>', '', b_content, flags=re.DOTALL)
b_content = re.sub(r'<!-- BottomNavBar \(Mobile Only\) -->.*?</nav>', '', b_content, flags=re.DOTALL)

# Insert new aside
my_aside = set_active_menu(standard_aside, "booking-mobil.html")
b_content = b_content.replace('<!-- Sidebar placeholder -->', my_aside)

# Insert new nav
my_nav = set_active_bottom_nav(standard_nav, "booking-mobil.html")
b_content = b_content.replace('</body>', f'{my_nav}\n</body>')

with open(booking_file, "w", encoding="utf-8") as f:
    f.write(b_content)
print("Updated booking-mobil.html")


# 2. Update riwayat.html
riwayat_file = os.path.join(base_dir, "riwayat.html")
with open(riwayat_file, "r", encoding="utf-8") as f:
    r_content = f.read()

r_content = re.sub(r'<!-- TopAppBar -->.*?</header>', standard_header, r_content, flags=re.DOTALL)
if '<div class="flex min-h-[calc(100vh-64px)]">' not in r_content:
    r_content = re.sub(r'(<main[^>]*>)', r'<div class="flex min-h-[calc(100vh-64px)]">\n    <!-- Sidebar placeholder -->\n    \1', r_content, count=1)
    r_content = re.sub(r'(</main>)', r'\1\n    </div>', r_content)

r_content = re.sub(r'<main[^>]*>', r'<main class="flex-1 lg:ml-72 pb-24 lg:pb-12 max-w-[1440px] mx-auto w-full">', r_content)
r_content = re.sub(r'<!-- Sidebar Navigation -->.*?</aside>', '', r_content, flags=re.DOTALL)
r_content = re.sub(r'<!-- BottomNavBar \(Mobile Only\) -->.*?</nav>', '', r_content, flags=re.DOTALL)

my_aside_r = set_active_menu(standard_aside, "riwayat.html")
r_content = r_content.replace('<!-- Sidebar placeholder -->', my_aside_r)

# Note: The bottom nav in riwayat is not defined if we strip it, let's insert before </body> or <script>
my_nav_r = set_active_bottom_nav(standard_nav, "riwayat.html")
# place it before <script src="../../controllers/api.js">
r_content = re.sub(r'(<script src="../../controllers/api\.js">)', rf'{my_nav_r}\n    \1', r_content)

with open(riwayat_file, "w", encoding="utf-8") as f:
    f.write(r_content)
print("Updated riwayat.html")

