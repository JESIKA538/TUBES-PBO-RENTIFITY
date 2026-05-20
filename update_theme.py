import os
import re
import shutil

# 1. Copy image
src_image = r'C:\Users\ASUS\.gemini\antigravity\brain\493b6c79-f4a1-4fe4-a1b7-c1f29b07dd10\jeje_profile_1779289689663.png'
dest_image = r'c:\TUBES PBO RENTIFITY\jeje_profile.png'
shutil.copy(src_image, dest_image)

dir_path = r'c:\TUBES PBO RENTIFITY'
old_img_url = 'https://lh3.googleusercontent.com/aida-public/AB6AXuCAubF20vKm-N4ZJ4_1hs9bpv0Vjx10ebDd0YjqHN9_7a_5lTsMhLahjcc6Yak7xrCrYShFAZAzYp7Zgf0yZoeCI2yA2PQ_ZMX0U7-kcnufS1dyjn0hrxzpPTowc3Fjmjx28OdI-Lz1rU3abIF8_oXsTZ49K72BH_-m3MgZvEuf8mt46r1VitzFt1WYruLUlZZxClBR9diSP_fznJmvYaDAAqgc_tOpu3j1Sl8ywQwTa_DWNqjLjnkpd_tAaTP-iz4jZmxsk55zV5s'

# Elegant palette matching light theme with luxury black/gold
elegant_colors = '''"colors": {
    "primary": "#18181b",
    "on-primary": "#ffffff",
    "primary-container": "#27272a",
    "on-primary-container": "#d4af37",
    "secondary": "#d4af37",
    "on-secondary": "#18181b",
    "secondary-container": "#fef08a",
    "on-secondary-container": "#422006",
    "tertiary": "#3f3f46",
    "on-tertiary": "#ffffff",
    "tertiary-container": "#e4e4e7",
    "on-tertiary-container": "#18181b",
    "error": "#ba1a1a",
    "on-error": "#ffffff",
    "error-container": "#ffdad6",
    "on-error-container": "#410002",
    "background": "#f8fafc",
    "on-background": "#0f172a",
    "surface": "#ffffff",
    "on-surface": "#0f172a",
    "surface-variant": "#e2e8f0",
    "on-surface-variant": "#475569",
    "outline": "#94a3b8",
    "outline-variant": "#cbd5e1",
    "inverse-surface": "#0f172a",
    "inverse-on-surface": "#f8fafc",
    "inverse-primary": "#d4af37",
    "surface-container-highest": "#e2e8f0",
    "surface-container-high": "#cbd5e1",
    "surface-container": "#f1f5f9",
    "surface-container-low": "#f8fafc",
    "surface-container-lowest": "#ffffff",
    "surface-dim": "#cbd5e1",
    "surface-bright": "#f8fafc",
    "surface-card": "#ffffff",
    "surface-bg": "#f8fafc",
    "primary-fixed": "#e4e4e7",
    "primary-fixed-dim": "#d4d4d8",
    "on-primary-fixed": "#18181b",
    "on-primary-fixed-variant": "#27272a",
    "secondary-fixed": "#fef08a",
    "secondary-fixed-dim": "#fde047",
    "on-secondary-fixed": "#422006",
    "on-secondary-fixed-variant": "#713f12",
    "warning-amber": "#d4af37"
}'''

# Replace colors in login and register specifically as well
simple_colors = '''colors: {
    primary: "#18181b", "primary-dark": "#09090b",
    secondary: "#d4af37", surface: "#ffffff",
    "on-surface": "#0f172a", "surface-variant": "#e2e8f0",
    "outline-variant": "#cbd5e1", "on-surface-variant": "#475569"
}'''

for filename in os.listdir(dir_path):
    if filename.endswith('.html'):
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update image
        content = content.replace(old_img_url, 'jeje_profile.png')

        # Replace full colors block (using regex to match the 'colors': {...} object)
        if '"colors": {' in content:
            content = re.sub(r'"colors":\s*{[^}]*}', elegant_colors, content, count=1, flags=re.DOTALL)
        elif 'colors: {' in content:
            content = re.sub(r'colors:\s*{[^}]*}', simple_colors, content, count=1, flags=re.DOTALL)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print('Updated theme and profile picture.')
