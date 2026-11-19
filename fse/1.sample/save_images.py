import base64
from bs4 import BeautifulSoup
from PIL import Image

with open('SET-MUK5KO3I-report.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

art0 = soup.find_all('article')[0]
for idx, img in enumerate(art0.find_all('img')):
    src = img.get('src', '')
    alt = img.get('alt', f'img_{idx}').replace(' ', '_')
    if ',' in src:
        header, b64data = src.split(',', 1)
        ext = 'png' if 'png' in header else ('gif' if 'gif' in header else 'bin')
        fname = f'test_q1_{idx}_{alt}.{ext}'
        with open(fname, 'wb') as out:
            out.write(base64.b64decode(b64data))
        im = Image.open(fname)
        print(f'Saved {fname}: format={im.format}, size={im.size}')
