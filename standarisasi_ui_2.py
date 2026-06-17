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
    inactive_cls = "text-on-surface-variant dark:text-surface-variant mx-2 my-1 px-4 py-3 flex items-center gap-3 hover:bg-surface-container-high rounded-lg transition-all"
    active_cls = "bg-secondary-container dark:bg-secondary text-on-secondary-container dark:text-on-secondary rounded-lg mx-2 my-1 px-4 py-3 flex items-center gap-3 active:scale-[0.99] transition-transform duration-150"
    nav_inner = re.search(r'(<nav class="flex-1 flex flex-col gap-1 px-2">.*?</nav>)', aside_html, re.DOTALL).group(1)
    nav_inner_reset = nav_inner.replace(active_cls, inactive_cls)
    nav_inner_reset = re.sub(r' style="font-variation-settings:\s*\'FILL\'\s*1;?"', '', nav_inner_reset)
    
    links = re.findall(r'<a.*?href="([^"]+)".*?</a>', nav_inner_reset, re.DOTALL)
    for link in links:
        if url_path in link:
            tag_match = re.search(rf'<a[^>]*href="{re.escape(link)}"[^>]*>.*?</a>', nav_inner_reset, re.DOTALL)
            if tag_match:
                tag = tag_match.group(0)
                new_tag = tag.replace(inactive_cls, active_cls)
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

# 3. detail-mobil.html
detail_file = os.path.join(base_dir, "detail-mobil.html")
with open(detail_file, "r", encoding="utf-8") as f:
    d_content = f.read()

# Replace header
if '<header' in d_content:
    d_content = re.sub(r'<header.*?</header>', standard_header, d_content, flags=re.DOTALL)

# Wrap main
if '<div class="flex min-h-[calc(100vh-64px)]">' not in d_content:
    d_content = re.sub(r'(<main[^>]*>)', r'<div class="flex min-h-[calc(100vh-64px)]">\n    <!-- Sidebar placeholder -->\n    \1', d_content, count=1)
    d_content = re.sub(r'(</main>)', r'\1\n    </div>', d_content)

# update main classes
d_content = re.sub(r'<main[^>]*>', r'<main class="flex-1 lg:ml-72 max-w-[1440px] mx-auto px-4 md:px-margin-desktop py-8 mb-24 lg:mb-0 w-full">', d_content)

# Replace sidebar and nav if they exist, or just insert
if '<!-- Sidebar Navigation -->' in d_content:
    d_content = re.sub(r'<!-- Sidebar Navigation -->.*?</aside>', '', d_content, flags=re.DOTALL)
if '<!-- BottomNavBar (Mobile Only) -->' in d_content:
    d_content = re.sub(r'<!-- BottomNavBar \(Mobile Only\) -->.*?</nav>', '', d_content, flags=re.DOTALL)

my_aside_d = set_active_menu(standard_aside, "daftar-mobil.html") # same as daftar-mobil since it's a sub-page of cars
d_content = d_content.replace('<!-- Sidebar placeholder -->', my_aside_d)

my_nav_d = set_active_bottom_nav(standard_nav, "daftar-mobil.html")
d_content = re.sub(r'(<script src="../../controllers/api\.js">)', rf'{my_nav_d}\n    \1', d_content)

with open(detail_file, "w", encoding="utf-8") as f:
    f.write(d_content)
print("Updated detail-mobil.html")

# 4. pembayaran.html
pembayaran_file = os.path.join(base_dir, "pembayaran.html")
with open(pembayaran_file, "r", encoding="utf-8") as f:
    p_content = f.read()

p_content = re.sub(r'<header.*?</header>', standard_header, p_content, flags=re.DOTALL)

if '<div class="flex min-h-[calc(100vh-64px)]">' not in p_content:
    p_content = re.sub(r'(<main[^>]*>)', r'<div class="flex min-h-[calc(100vh-64px)]">\n    <!-- Sidebar placeholder -->\n    \1', p_content, count=1)
    p_content = re.sub(r'(</main>)', r'\1\n    </div>', p_content)

p_content = re.sub(r'<main[^>]*>', r'<main class="flex-1 lg:ml-72 max-w-[1440px] mx-auto px-4 md:px-margin-desktop py-8 mb-24 lg:mb-0 w-full grid lg:grid-cols-12 gap-6">', p_content)

my_aside_p = set_active_menu(standard_aside, "riwayat.html")
p_content = p_content.replace('<!-- Sidebar placeholder -->', my_aside_p)

my_nav_p = set_active_bottom_nav(standard_nav, "riwayat.html")
p_content = re.sub(r'(<script src="../../controllers/api\.js">)', rf'{my_nav_p}\n    \1', p_content)

with open(pembayaran_file, "w", encoding="utf-8") as f:
    f.write(p_content)
print("Updated pembayaran.html")

# 5. pengaturan-user.html
pengaturan_file = os.path.join(base_dir, "pengaturan-user.html")
with open(pengaturan_file, "r", encoding="utf-8") as f:
    pu_content = f.read()

pu_content = re.sub(r'<!-- Header -->\s*<header.*?</header>', standard_header, pu_content, flags=re.DOTALL)

if '<div class="flex min-h-[calc(100vh-64px)]">' not in pu_content:
    pu_content = re.sub(r'(<main[^>]*>)', r'<div class="flex min-h-[calc(100vh-64px)]">\n    <!-- Sidebar placeholder -->\n    \1', pu_content, count=1)
    pu_content = re.sub(r'(</main>)', r'\1\n    </div>', pu_content)

# in pengaturan-user.html, the main tag contains the sidebar. Let's remove the old sidebar!
pu_content = re.sub(r'<!-- Sidebar Navigation \(Hidden on Mobile\) -->\s*<nav.*?</nav>', '', pu_content, flags=re.DOTALL)
# also remove the wrapper if it was using flex inside main. Actually, let's check its layout later. We'll set main class.
pu_content = re.sub(r'<main[^>]*>', r'<main class="flex-1 lg:ml-72 max-w-[1440px] mx-auto px-4 md:px-margin-desktop py-8 mb-24 lg:mb-0 w-full flex flex-col md:flex-row gap-8">', pu_content)

my_aside_pu = set_active_menu(standard_aside, "pengaturan-user.html")
pu_content = pu_content.replace('<!-- Sidebar placeholder -->', my_aside_pu)

pu_content = re.sub(r'<!-- Bottom Navigation Bar \(Mobile Only\) -->\s*<nav.*?</nav>', '', pu_content, flags=re.DOTALL)
my_nav_pu = set_active_bottom_nav(standard_nav, "pengaturan-user.html")
pu_content = re.sub(r'(<script src="../../controllers/api\.js">)', rf'{my_nav_pu}\n    \1', pu_content)

with open(pengaturan_file, "w", encoding="utf-8") as f:
    f.write(pu_content)
print("Updated pengaturan-user.html")
