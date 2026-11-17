import os
import urllib.request
import ssl
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

out_dir = Path("assets/images")
out_dir.mkdir(parents=True, exist_ok=True)

downloads = [
    ("logo.png", "https://golodnyimykola.com.ua/images/logo.png"),
    ("favicon.png", "https://golodnyimykola.com.ua/images/favicon.png"),
    ("hero_bg.webp", "https://cdn-media.choiceqr.com/prod-eat-golodnyimykola/background-image/QZInlHx-SkFyPCh-FyhImFn_original.webp"),
    ("restaurant_ext.jpg", "https://golodnyimykola.com.ua/images/bagallery/gallery-1/thumbnail/category-1/DSCF3332.jpg"),
    ("restaurant_lake.jpg", "https://golodnyimykola.com.ua/images/bagallery/gallery-1/thumbnail/category-1/18891462_816419931848874_2927886141123211426_o.jpg"),
    ("hall_urochysta.jpeg", "https://golodnyimykola.com.ua/images/bagallery/gallery-1/thumbnail/category-2/1-DSC_6948.jpeg"),
    ("hall_kamin.jpeg", "https://golodnyimykola.com.ua/images/bagallery/gallery-1/thumbnail/category-2/1-DSC_6983.jpeg"),
    ("hall_interior.jpeg", "https://golodnyimykola.com.ua/images/bagallery/gallery-1/thumbnail/category-2/4-DSC_6950.jpeg"),
    ("terrace.jpg", "https://golodnyimykola.com.ua/images/bagallery/gallery-1/thumbnail/category-1/11111156_483910238433180_1486348673358465890_o.jpg"),
    ("kids_farm.jpg", "https://golodnyimykola.com.ua/images/bagallery/gallery-1/thumbnail/category-1/1908475_415825531908318_5365373762593402241_n.jpg"),
    ("celebration.jpg", "https://golodnyimykola.com.ua/images/bagallery/gallery-1/thumbnail/category-1/80280568_1481773495313511_6489420732118859776_o.jpg"),
    ("shop_craft.jpg", "https://golodnyimykola.com.ua/images/services/64751004_1323470344477161_550243017798189056_n.jpg"),
    ("corporate_hall.jpg", "https://golodnyimykola.com.ua/images/IMG_7896.jpg"),
    ("dinner_ambiance.jpg", "https://golodnyimykola.com.ua/images/services/81369410_1499173693573491_7972413153482899456_o.jpg"),
]

for filename, url in downloads:
    dest = out_dir / filename
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            content = resp.read()
            with open(dest, "wb") as f:
                f.write(content)
            print(f"Downloaded {filename} ({len(content)} bytes)")
    except Exception as e:
        print(f"Failed {filename}: {e}")

print("Assets download completed.")
