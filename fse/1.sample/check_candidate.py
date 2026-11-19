from bs4 import BeautifulSoup

with open('SET-MUK5KO3I-report.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

articles = soup.find_all('article')
for i, art in enumerate(articles):
    pres = art.find_all('pre')
    js_code = pres[2].text if len(pres) > 2 else ''
    lines = [line.strip() for line in js_code.splitlines() if line.strip()]
    # check how many lines in event listener
    non_comment_lines = [l for l in lines if not l.startswith('//') and not l.startswith('/*')]
    print(f"Q{i+1}: total lines={len(lines)}, non-comment={len(non_comment_lines)}")
