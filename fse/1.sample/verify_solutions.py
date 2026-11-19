import json
from bs4 import BeautifulSoup
from create_solutions import solutions

with open('SET-MUK5KO3I-report.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

articles = soup.find_all('article')
assert len(articles) == 29

all_passed = True

for i, art in enumerate(articles):
    q_num = i + 1
    pres = art.find_all('pre')
    html_code = pres[0].text
    css_code = pres[1].text
    js_code = pres[2].text
    
    sol = solutions[q_num]
    
    # HTML check
    h_target, h_repl = sol["html_replace"]
    # normalize newlines for matching
    h_target_norm = h_target.replace('\r\n', '\n')
    html_code_norm = html_code.replace('\r\n', '\n')
    if h_target_norm not in html_code_norm:
        print(f"FAILED HTML match for Q{q_num}")
        print("Target was:\n", repr(h_target_norm))
        all_passed = False
    else:
        new_html = html_code_norm.replace(h_target_norm, h_repl)
        if 'TODO' in new_html:
            print(f"WARNING: TODO still in HTML for Q{q_num}")

    # CSS check
    c_target, c_repl = sol["css_replace"]
    c_target_norm = c_target.replace('\r\n', '\n')
    css_code_norm = css_code.replace('\r\n', '\n')
    if c_target_norm not in css_code_norm:
        print(f"FAILED CSS match for Q{q_num}")
        print("Target was:\n", repr(c_target_norm))
        all_passed = False
    else:
        new_css = css_code_norm.replace(c_target_norm, c_repl)
        if 'TODO' in new_css:
            print(f"WARNING: TODO still in CSS for Q{q_num}")

    # JS check
    j_target, j_repl = sol["js_replace"]
    j_target_norm = j_target.replace('\r\n', '\n')
    js_code_norm = js_code.replace('\r\n', '\n')
    if j_target_norm not in js_code_norm:
        print(f"FAILED JS match for Q{q_num}")
        print("Target was:\n", repr(j_target_norm))
        all_passed = False
    else:
        new_js = js_code_norm.replace(j_target_norm, j_repl)
        if 'TODO' in new_js:
            print(f"WARNING: TODO still in JS for Q{q_num}")

if all_passed:
    print("ALL 29 QUESTIONS PASSED REPLACEMENT CHECKS WITH ZERO ERRORS!")
