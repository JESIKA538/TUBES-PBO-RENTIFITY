import re

with open(r'c:\TUBES PBO RENTIFITY\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We know there are 3 hardcoded cars. We can find the buttons.
# They look like:
# <button
# class="flex-1 bg-primary text-on-primary py-3 rounded-lg font-label-md hover:opacity-90 transition-opacity">Pesan
# Sekarang</button>

# First car (Porsche) -> id=1
# Second car (BMW) -> id=2
# Third car (Tesla) -> id=3

# Let's replace the 3 occurrences with <a> tags.
count = 1
def replacer(match):
    global count
    car_id = count
    count += 1
    # Return an <a> tag pointing to detail-mobil.html?id=... with "Lihat Detail"
    return f'<button onclick="window.location.href=\'detail-mobil.html?id={car_id}\'" ' + match.group(1) + '>Lihat Detail</button>'

# Match the <button followed by class="..." then >Pesan \n Sekarang</button>
new_content = re.sub(
    r'<button\s+(class="flex-1 bg-primary text-on-primary py-3 rounded-lg font-label-md hover:opacity-90 transition-opacity")>\s*Pesan\s*Sekarang\s*</button>',
    replacer,
    content
)

# Wait, the class might have different whitespace. Let's just match any <button class="...">Pesan\s*Sekarang</button>
new_content2 = re.sub(
    r'<button\s+([^>]+)>\s*Pesan\s*Sekarang\s*</button>',
    replacer,
    content
)

with open(r'c:\TUBES PBO RENTIFITY\index.html', 'w', encoding='utf-8') as f:
    f.write(new_content2)

print(f"Replaced {count-1} occurrences.")
