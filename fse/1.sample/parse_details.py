import re
from bs4 import BeautifulSoup

with open('SET-MUK5KO3I-report.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

articles = soup.find_all('article')

with open('all_todos_detailed.txt', 'w', encoding='utf-8') as out:
    for i, art in enumerate(articles):
        title = art.find('h2').text.strip()
        pres = art.find_all('pre')
        html_code = pres[0].text if len(pres) > 0 else ''
        css_code = pres[1].text if len(pres) > 1 else ''
        js_code = pres[2].text if len(pres) > 2 else ''
        
        sub_soup = BeautifulSoup(html_code, 'html.parser')
        html_title = sub_soup.title.text.strip() if sub_soup.title else ''
        
        out.write(f"==========================================================\n")
        out.write(f"QUESTION {i+1}: {title} ({html_title})\n")
        out.write(f"==========================================================\n")
        
        # HTML TODOs
        out.write("--- HTML TODOs ---\n")
        for m in re.finditer(r'<!--\s*(TODO.*?)\s*-->', html_code, re.DOTALL):
            start = max(0, m.start() - 100)
            end = min(len(html_code), m.end() + 200)
            out.write(f"Comment: {m.group(1)}\n")
            out.write(f"Context:\n{html_code[start:end]}\n\n")
            
        # CSS TODOs
        out.write("--- CSS TODOs ---\n")
        for m in re.finditer(r'/\*\s*(TODO.*?)\s*\*/', css_code, re.DOTALL):
            start = max(0, m.start() - 100)
            end = min(len(css_code), m.end() + 100)
            out.write(f"Comment: {m.group(1)}\n")
            out.write(f"Context:\n{css_code[start:end]}\n\n")

        # JS TODOs
        out.write("--- JS TODOs ---\n")
        for m in re.finditer(r'(//\s*TODO.*(?:\n\s*//.*)*)', js_code):
            out.write(f"Comment:\n{m.group(1)}\n\n")
        for m in re.finditer(r'/\*\s*(TODO.*?)\s*\*/', js_code, re.DOTALL):
            out.write(f"Block Comment:\n{m.group(1)}\n\n")
            
        out.write("\n")
print("Saved all_todos_detailed.txt")
