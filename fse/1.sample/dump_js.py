from bs4 import BeautifulSoup

with open('SET-MUK5KO3I-report.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

articles = soup.find_all('article')

for i, art in enumerate(articles):
    title = art.find('h2').text.strip()
    pres = art.find_all('pre')
    js_code = pres[2].text if len(pres) > 2 else ''
    print(f"=== {title} ===")
    print(js_code)
    print("-" * 50)
