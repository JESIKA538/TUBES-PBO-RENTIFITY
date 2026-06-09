import os
import re

new_colors = '''"colors": {
    "primary": "#1C2E4A",
    "on-primary": "#ffffff",
    "primary-container": "#0F1A2B",
    "on-primary-container": "#BDC4D4",
    "secondary": "#52677D",
    "on-secondary": "#ffffff",
    "secondary-container": "#BDC4D4",
    "on-secondary-container": "#0F1A2B",
    "tertiary": "#52677D",
    "on-tertiary": "#ffffff",
    "tertiary-container": "#BDC4D4",
    "on-tertiary-container": "#1C2E4A",
    "error": "#ba1a1a",
    "on-error": "#ffffff",
    "error-container": "#ffdad6",
    "on-error-container": "#410002",
    "background": "#D1CFC9",
    "on-background": "#0F1A2B",
    "surface": "#ffffff",
    "on-surface": "#0F1A2B",
    "surface-variant": "#BDC4D4",
    "on-surface-variant": "#1C2E4A",
    "outline": "#52677D",
    "outline-variant": "#BDC4D4",
    "inverse-surface": "#0F1A2B",
    "inverse-on-surface": "#D1CFC9",
    "inverse-primary": "#52677D",
    "surface-container-highest": "#BDC4D4",
    "surface-container-high": "#D1CFC9",
    "surface-container": "#ffffff",
    "surface-container-low": "#ffffff",
    "surface-container-lowest": "#ffffff",
    "surface-dim": "#BDC4D4",
    "surface-bright": "#ffffff",
    "surface-card": "#ffffff",
    "surface-bg": "#D1CFC9",
    "primary-fixed": "#BDC4D4",
    "primary-fixed-dim": "#52677D",
    "on-primary-fixed": "#0F1A2B",
    "on-primary-fixed-variant": "#1C2E4A",
    "secondary-fixed": "#BDC4D4",
    "secondary-fixed-dim": "#52677D",
    "on-secondary-fixed": "#0F1A2B",
    "on-secondary-fixed-variant": "#1C2E4A",
    "warning-amber": "#1C2E4A"
}'''

directory = r"c:\TUBES PBO RENTIFITY"
html_files = [f for f in os.listdir(directory) if f.endswith('.html')]

for filename in html_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to match the colors block
    # It starts with "colors": { and ends with }, matching anything in between non-greedily
    pattern = r'"colors"\s*:\s*\{.*?\}(?=\s*,\s*"borderRadius"|\s*\})'
    
    new_content = re.sub(pattern, new_colors, content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

print(f"Updated colors in {len(html_files)} HTML files.")
