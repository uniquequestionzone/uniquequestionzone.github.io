import os
from bs4 import BeautifulSoup

with open('SET-MUK5KO3I-report.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

articles = soup.find_all('article')
print(f"Total questions: {len(articles)}")

for i, art in enumerate(articles):
    title = art.find('h2').text.strip()
    pres = art.find_all('pre')
    html_code = pres[0].text if len(pres) > 0 else ''
    css_code = pres[1].text if len(pres) > 1 else ''
    js_code = pres[2].text if len(pres) > 2 else ''
    sub_soup = BeautifulSoup(html_code, 'html.parser')
    html_title = sub_soup.title.text.strip() if sub_soup.title else ''
    
    # check images
    imgs = art.find_all('img')
    img_alts = [img.get('alt', '') for img in imgs]
    
    print(f"[{i+1}] {title} | Title: '{html_title}' | HTML: {len(html_code)}b | CSS: {len(css_code)}b | JS: {len(js_code)}b | Imgs: {img_alts}")
