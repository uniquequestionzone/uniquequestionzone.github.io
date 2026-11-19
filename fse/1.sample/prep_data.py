import json
import html
from bs4 import BeautifulSoup
from create_solutions import solutions

with open('SET-MUK5KO3I-report.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

articles = soup.find_all('article')
assert len(articles) == 29

questions_data = []

for i, art in enumerate(articles):
    q_num = i + 1
    h2 = art.find('h2').text.strip()
    pres = art.find_all('pre')
    raw_html = pres[0].text
    raw_css = pres[1].text
    raw_js = pres[2].text
    
    sol = solutions[q_num]
    
    h_target, h_repl = sol["html_replace"]
    c_target, c_repl = sol["css_replace"]
    j_target, j_repl = sol["js_replace"]
    
    solved_html = raw_html.replace(h_target.replace('\r\n', '\n'), h_repl)
    solved_css = raw_css.replace(c_target.replace('\r\n', '\n'), c_repl)
    solved_js = raw_js.replace(j_target.replace('\r\n', '\n'), j_repl)
    
    # parse title, badge, tagline from html
    sub_soup = BeautifulSoup(raw_html, 'html.parser')
    page_title = sub_soup.title.text.strip() if sub_soup.title else h2
    badge_el = sub_soup.find(class_='badge')
    badge = badge_el.text.strip() if badge_el else 'Front-End'
    tagline_el = sub_soup.find(class_='tagline')
    tagline = tagline_el.text.strip() if tagline_el else ''
    
    questions_data.append({
        "num": q_num,
        "title": page_title,
        "badge": badge,
        "tagline": tagline,
        "h_target": h_target,
        "h_repl": h_repl,
        "c_target": c_target,
        "c_repl": c_repl,
        "j_target": j_target,
        "j_repl": j_repl,
        "solved_html": solved_html,
        "solved_css": solved_css,
        "solved_js": solved_js,
    })

print(f"Prepared data for {len(questions_data)} questions.")
