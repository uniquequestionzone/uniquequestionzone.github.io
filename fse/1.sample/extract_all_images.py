import os
import base64
from bs4 import BeautifulSoup

os.makedirs('images', exist_ok=True)

with open('SET-MUK5KO3I-report.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

articles = soup.find_all('article')

for i, art in enumerate(articles):
    for idx, img in enumerate(art.find_all('img')):
        alt = img.get('alt', f'img_{idx}').replace(' ', '_')
        src = img.get('src', '')
        if ',' in src:
            header, b64data = src.split(',', 1)
            ext = 'png' if 'png' in header else ('gif' if 'gif' in header else 'bin')
            fname = f'images/q{i+1}_{idx}_{alt}.{ext}'
            with open(fname, 'wb') as out:
                out.write(base64.b64decode(b64data))

print(f"Saved all images for {len(articles)} questions to images/")
