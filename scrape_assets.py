import urllib.request
import ssl
import re
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    'https://golodnyimykola.com.ua/',
    'https://golodnyimykola.com.ua/khto-my',
    'https://golodnyimykola.com.ua/posluhy/simeinyi-vidpochynok-z-ditmy',
    'https://golodnyimykola.com.ua/posluhy/vesillia',
    'https://golodnyimykola.com.ua/posluhy/benkety-iuvilei-ta-dni-narodzhennia',
    'https://golodnyimykola.com.ua/posluhy/korporatyvy',
    'https://golodnyimykola.com.ua/posluhy/kramnytsia',
    'https://golodnyimykola.com.ua/posluhy/dostavka',
    'https://golodnyimykola.com.ua/posluhy/zatyshni-vecheri',
    'https://golodnyimykola.com.ua/posluhy/konferentsii',
    'https://golodnyimykola.com.ua/menu'
]

found_imgs = set()
for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, context=ctx, timeout=10).read().decode('utf-8', errors='ignore')
        matches = re.findall(r'(/images/[a-zA-Z0-9_\-\./]+\.(?:jpg|jpeg|png|webp|svg))', html, re.IGNORECASE)
        for m in matches:
            found_imgs.add(m)
        # also find any other external or choiceqr images
        ext_matches = re.findall(r'(https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp))', html, re.IGNORECASE)
        for em in ext_matches:
            if 'choiceqr' in em or 'golodnyimykola' in em:
                found_imgs.add(em)
    except Exception as e:
        print(f"Error fetching {u}: {e}")

print(f"Total unique images found: {len(found_imgs)}")
results = sorted(list(found_imgs))
with open('extracted_images.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

for img in results[:30]:
    print(img)
