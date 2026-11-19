import re
from bs4 import BeautifulSoup

with open('SET-MUK5KO3I-report.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

articles = soup.find_all('article')

for i, art in enumerate(articles):
    title_el = art.find('h2')
    title = title_el.text.strip() if title_el else f"Question {i+1}"
    pres = art.find_all('pre')
    html_code = pres[0].text if len(pres) > 0 else ''
    css_code = pres[1].text if len(pres) > 1 else ''
    js_code = pres[2].text if len(pres) > 2 else ''
    
    sub_soup = BeautifulSoup(html_code, 'html.parser')
    html_title = sub_soup.title.text.strip() if sub_soup.title else ''
    
    html_todos = re.findall(r'<!--\s*(TODO.*?)\s*-->', html_code, re.DOTALL | re.IGNORECASE)
    css_todos = re.findall(r'/\*\s*(TODO.*?)\s*\*/', css_code, re.DOTALL | re.IGNORECASE)
    js_todos = re.findall(r'//\s*(TODO.*?)$', js_code, re.MULTILINE | re.IGNORECASE)
    js_block_todos = re.findall(r'/\*\s*(TODO.*?)\s*\*/', js_code, re.DOTALL | re.IGNORECASE)
    
    print(f"==================================================")
    print(f"[{i+1}] {title}: '{html_title}'")
    print(f"  HTML TODOs ({len(html_todos)}): {html_todos}")
    print(f"  CSS  TODOs ({len(css_todos)}): {css_todos}")
    print(f"  JS   TODOs ({len(js_todos) + len(js_block_todos)}): {js_todos + js_block_todos}")
