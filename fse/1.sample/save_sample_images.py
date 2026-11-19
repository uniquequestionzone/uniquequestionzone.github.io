import base64
from bs4 import BeautifulSoup
from PIL import Image

with open('SET-MUK5KO3I-report.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

articles = soup.find_all('article')

for q_num in [2, 3, 4, 11, 20]:
    art = articles[q_num - 1]
    for idx, img in enumerate(art.find_all('img')):
        src = img.get('src', '')
        alt = img.get('alt', f'img_{idx}').replace(' ', '_')
        if ',' in src and 'png' in src:
            header, b64data = src.split(',', 1)
            fname = f'test_q{q_num}_{idx}_{alt}.png'
            with open(fname, 'wb') as out:
                out.write(base64.b64decode(b64data))
            print(f'Saved {fname}')
