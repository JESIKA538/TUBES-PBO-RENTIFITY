import os

file_path = r"c:\TUBES PBO RENTIFITY\pembayaran.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

replacements = {
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Bank_Central_Asia.svg/2560px-Bank_Central_Asia.svg.png": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Bank_Central_Asia.svg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Bank_Mandiri_logo_2016.svg/2560px-Bank_Mandiri_logo_2016.svg.png": "https://upload.wikimedia.org/wikipedia/commons/a/ad/Bank_Mandiri_logo_2016.svg",
    "https://upload.wikimedia.org/wikipedia/id/thumb/5/55/BNI_logo.svg/2560px-BNI_logo.svg.png": "https://upload.wikimedia.org/wikipedia/id/5/55/BNI_logo.svg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/BRI_2020.svg/2560px-BRI_2020.svg.png": "https://upload.wikimedia.org/wikipedia/commons/2/2e/BRI_2020.svg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Gopay_logo.svg/2560px-Gopay_logo.svg.png": "https://upload.wikimedia.org/wikipedia/commons/8/86/Gopay_logo.svg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/OVO_Logo.svg/2560px-OVO_Logo.svg.png": "https://upload.wikimedia.org/wikipedia/commons/e/e4/OVO_Logo.svg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Logo_dana_blue.svg/2560px-Logo_dana_blue.svg.png": "https://upload.wikimedia.org/wikipedia/commons/7/72/Logo_dana_blue.svg"
}

for old_url, new_url in replacements.items():
    html = html.replace(old_url, new_url)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Logos fixed.")
