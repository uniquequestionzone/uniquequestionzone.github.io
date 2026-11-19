import json
import html
import re
from bs4 import BeautifulSoup
from create_solutions import solutions

with open('SET-MUK5KO3I-report.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

articles = soup.find_all('article')
assert len(articles) == 29

question_entries = []

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
    
    # Combined document for iframe live demo:
    # inline CSS and JS into HTML
    demo_doc = solved_html.replace('<link rel="stylesheet" href="index.css">', f'<style>\n{solved_css}\n</style>')
    demo_doc = demo_doc.replace('<script src="index.js"></script>', f'<script>\n{solved_js}\n</script>')
    
    question_entries.append({
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
        "demo_doc": demo_doc
    })

print(f"Processed {len(question_entries)} questions.")

# Now build the HTML page
html_output = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover">
    <meta name="theme-color" content="#4F46E5">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <title>Assessment Solutions & Live Outputs - All 29 Questions</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #4F46E5;
            --primary-hover: #4338CA;
            --primary-light: #EEF2FF;
            --primary-100: #E0E7FF;
            --success: #10B981;
            --success-light: #ECFDF5;
            --warning: #F59E0B;
            --warning-light: #FEF3C7;
            --danger: #EF4444;
            --dark: #0F172A;
            --slate-800: #1E293B;
            --slate-700: #334155;
            --slate-600: #475569;
            --slate-500: #64748B;
            --slate-400: #94A3B8;
            --slate-300: #CBD5E1;
            --slate-200: #E2E8F0;
            --slate-100: #F1F5F9;
            --slate-50: #F8FAFC;
            --code-bg: #181825;
            --code-text: #CDD6F4;
            --sidebar-width: 320px;
            --mobile-nav-height: 56px;
            --safe-bottom: env(safe-area-inset-bottom, 0px);
        }

        *, *::before, *::after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        html {
            scroll-behavior: smooth;
            -webkit-text-size-adjust: 100%;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #F8FAFC;
            color: var(--dark);
            line-height: 1.6;
            display: flex;
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
        }

        /* Mobile Sticky Topbar (Shown on Mobile / Tablet) */
        .mobile-topbar {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: var(--mobile-nav-height);
            background: rgba(255, 255, 255, 0.96);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--slate-200);
            z-index: 900;
            padding: 0 12px;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }

        .mobile-topbar-left {
            display: flex;
            align-items: center;
            gap: 10px;
            min-width: 0;
        }

        .icon-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 38px;
            height: 38px;
            background: transparent;
            border: 1px solid var(--slate-200);
            border-radius: 8px;
            color: var(--slate-700);
            cursor: pointer;
            touch-action: manipulation;
            transition: all 0.15s ease;
            flex-shrink: 0;
        }

        .icon-btn:hover, .icon-btn:active {
            background: var(--slate-100);
            color: var(--primary);
            border-color: var(--primary-100);
        }

        .mobile-brand {
            font-size: 15px;
            font-weight: 800;
            color: var(--primary);
            display: flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .mobile-active-pill {
            background: var(--primary-light);
            color: var(--primary);
            font-size: 11px;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 999px;
            white-space: nowrap;
        }

        .mobile-topbar-right {
            display: flex;
            align-items: center;
            gap: 6px;
            flex-shrink: 0;
        }

        /* Sidebar Navigation Drawer */
        .sidebar {
            width: var(--sidebar-width);
            background: #FFFFFF;
            border-right: 1px solid var(--slate-200);
            height: 100vh;
            position: sticky;
            top: 0;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            flex-shrink: 0;
            z-index: 1000;
            transition: transform 0.28s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .sidebar-header {
            padding: 20px 20px 16px;
            border-bottom: 1px solid var(--slate-200);
            background: #FFFFFF;
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 8px;
        }

        .sidebar-header-info {
            min-width: 0;
        }

        .sidebar-header h1 {
            font-size: 17px;
            font-weight: 800;
            color: var(--primary);
            display: flex;
            align-items: center;
            gap: 8px;
            letter-spacing: -0.3px;
        }

        .sidebar-header p {
            font-size: 12px;
            color: var(--slate-500);
            margin-top: 3px;
        }

        .sidebar-close-btn {
            display: none;
            background: none;
            border: none;
            color: var(--slate-500);
            font-size: 20px;
            cursor: pointer;
            padding: 4px;
            touch-action: manipulation;
        }

        .sidebar-tools {
            padding: 12px 16px;
            border-bottom: 1px solid var(--slate-200);
            background: var(--slate-50);
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .sidebar-search-wrap {
            position: relative;
            width: 100%;
        }

        .sidebar-search-wrap input {
            width: 100%;
            padding: 8px 30px 8px 12px;
            font-size: 13px;
            border: 1px solid var(--slate-200);
            border-radius: 8px;
            outline: none;
            background: #FFFFFF;
            transition: all 0.2s;
            font-family: inherit;
        }

        .sidebar-search-wrap input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
        }

        .clear-search-btn {
            position: absolute;
            right: 8px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: var(--slate-400);
            cursor: pointer;
            font-size: 14px;
            padding: 2px 4px;
            display: none;
        }

        .filter-chips {
            display: flex;
            gap: 4px;
            overflow-x: auto;
            scrollbar-width: none;
            padding-bottom: 2px;
        }
        .filter-chips::-webkit-scrollbar { display: none; }

        .chip-btn {
            background: #FFFFFF;
            border: 1px solid var(--slate-200);
            border-radius: 999px;
            padding: 3px 9px;
            font-size: 11px;
            font-weight: 600;
            color: var(--slate-600);
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.15s ease;
            touch-action: manipulation;
        }

        .chip-btn:hover, .chip-btn.active {
            background: var(--primary-light);
            color: var(--primary);
            border-color: var(--primary);
        }


        .sidebar-menu {
            overflow-y: auto;
            flex: 1;
            padding: 10px 12px;
            -webkit-overflow-scrolling: touch;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 10px;
            margin-bottom: 3px;
            border-radius: 8px;
            text-decoration: none;
            color: var(--slate-700);
            font-size: 13px;
            font-weight: 500;
            transition: all 0.15s;
            touch-action: manipulation;
        }

        .nav-item:hover {
            background: var(--slate-100);
            color: var(--primary);
        }

        .nav-item.active {
            background: var(--primary-light);
            color: var(--primary);
            font-weight: 700;
        }

        .nav-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 24px;
            height: 24px;
            background: var(--slate-100);
            color: var(--slate-600);
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            flex-shrink: 0;
        }

        .nav-item.active .nav-badge {
            background: var(--primary);
            color: #FFFFFF;
        }

        .nav-title {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-size: 12.5px;
        }

        /* Sidebar Backdrop for Mobile */
        .sidebar-backdrop {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(15, 23, 42, 0.5);
            backdrop-filter: blur(3px);
            -webkit-backdrop-filter: blur(3px);
            z-index: 950;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.25s ease;
        }

        .sidebar-backdrop.active {
            opacity: 1;
            pointer-events: auto;
        }

        /* Main Content */
        .main-wrapper {
            flex: 1;
            min-width: 0;
            padding: 32px 40px 60px;
            max-width: 1240px;
            margin: 0 auto;
            width: 100%;
        }

        /* Hero Banner */
        .hero-banner {
            background: linear-gradient(135deg, #4338CA 0%, #6366F1 50%, #8B5CF6 100%);
            color: #FFFFFF;
            padding: 36px 36px;
            border-radius: 16px;
            margin-bottom: 36px;
            box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.25);
            position: relative;
            overflow: hidden;
        }

        .hero-banner h1 {
            font-size: clamp(22px, 3.5vw, 30px);
            font-weight: 900;
            letter-spacing: -0.5px;
            margin-bottom: 10px;
            line-height: 1.25;
        }

        .hero-banner p {
            font-size: 14.5px;
            opacity: 0.95;
            max-width: 820px;
            line-height: 1.6;
        }


        /* Question Section Card */
        .q-card {
            background: #FFFFFF;
            border: 1px solid var(--slate-200);
            border-radius: 16px;
            margin-bottom: 36px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            scroll-margin-top: 32px;
            overflow: hidden;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        .q-card:hover {
            box-shadow: 0 10px 20px -3px rgba(0, 0, 0, 0.07);
            border-color: #CBD5E1;
        }

        .q-header {
            padding: 22px 28px;
            border-bottom: 1px solid var(--slate-200);
            background: #FFFFFF;
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 14px;
        }

        .q-title-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
            min-width: 0;
        }

        .q-tags {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 6px;
        }

        .q-badge {
            background: var(--primary-light);
            color: var(--primary);
            padding: 3px 9px;
            border-radius: 999px;
            font-size: 11.5px;
            font-weight: 700;
        }

        .q-num {
            background: var(--dark);
            color: #FFFFFF;
            padding: 3px 9px;
            border-radius: 6px;
            font-size: 11.5px;
            font-weight: 800;
        }

        .q-verified-badge {
            background: var(--success-light);
            color: #047857;
            padding: 3px 8px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        .q-header h2 {
            font-size: 21px;
            font-weight: 800;
            color: var(--dark);
            line-height: 1.3;
        }

        .q-tagline {
            font-size: 13.5px;
            color: var(--slate-500);
            line-height: 1.5;
        }

        /* Tabs */
        .tabs-bar {
            display: flex;
            background: var(--slate-50);
            border-bottom: 1px solid var(--slate-200);
            padding: 6px 16px;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: none;
            gap: 4px;
        }
        .tabs-bar::-webkit-scrollbar { display: none; }

        .tab-btn {
            background: transparent;
            border: none;
            padding: 10px 14px;
            font-size: 12.5px;
            font-weight: 600;
            color: var(--slate-600);
            cursor: pointer;
            border-radius: 8px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.15s;
            white-space: nowrap;
            touch-action: manipulation;
            font-family: inherit;
        }

        .tab-btn:hover {
            color: var(--primary);
            background: rgba(79, 70, 229, 0.05);
        }

        .tab-btn.active {
            color: var(--primary);
            background: #FFFFFF;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            font-weight: 700;
        }

        .tab-pane {
            display: none;
            padding: 22px 28px;
        }

        .tab-pane.active {
            display: block;
        }

        /* Changes Overview Box */
        .change-box {
            background: var(--slate-50);
            border: 1px solid var(--slate-200);
            border-radius: 12px;
            padding: 16px 18px;
            margin-bottom: 16px;
        }

        .change-box h4 {
            font-size: 13.5px;
            font-weight: 700;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .change-box.html h4 { color: #EA580C; }
        .change-box.css h4 { color: #0284C7; }
        .change-box.js h4 { color: #16A34A; }

        .diff-view {
            display: grid;
            grid-template-columns: 1fr;
            gap: 10px;
            font-family: 'Fira Code', Consolas, Monaco, monospace;
            font-size: 12.5px;
        }

        .diff-item {
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--slate-200);
        }

        .diff-label {
            padding: 5px 12px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .diff-before .diff-label {
            background: #FEE2E2;
            color: #991B1B;
        }

        .diff-after .diff-label {
            background: #DCFCE7;
            color: #166534;
        }

        .diff-code {
            padding: 10px 14px;
            background: #FFFFFF;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            white-space: pre;
            line-height: 1.5;
        }

        /* Code Blocks */
        .code-container {
            position: relative;
            background: var(--code-bg);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .code-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 16px;
            background: #11111b;
            border-bottom: 1px solid #313244;
            color: #A6ADC8;
            font-size: 12px;
            font-family: 'Fira Code', Consolas, monospace;
        }

        .copy-btn {
            background: #313244;
            color: #CDD6F4;
            border: none;
            padding: 5px 12px;
            font-size: 11.5px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.15s;
            touch-action: manipulation;
        }

        .copy-btn:hover, .copy-btn:active {
            background: var(--primary);
            color: #FFFFFF;
        }

        pre.code-block {
            margin: 0;
            padding: 16px 18px;
            color: var(--code-text);
            font-family: 'Fira Code', Consolas, monospace;
            font-size: 12.5px;
            line-height: 1.55;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            max-height: 480px;
        }

        /* Live Preview Frame */
        .preview-container {
            background: #FFF;
            border: 1px solid var(--slate-200);
            border-radius: 12px;
            padding: 14px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .preview-toolbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12.5px;
            color: var(--slate-600);
            font-weight: 600;
            flex-wrap: wrap;
            gap: 8px;
        }

        .preview-actions {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .preview-frame {
            width: 100%;
            height: 460px;
            border: 1px solid var(--slate-200);
            border-radius: 8px;
            background: #FFFFFF;
        }

        /* Card Footer Nav */
        .card-footer-nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 20px;
            background: var(--slate-50);
            border-top: 1px solid var(--slate-200);
            gap: 10px;
        }

        .footer-nav-btn {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #FFFFFF;
            border: 1px solid var(--slate-200);
            color: var(--slate-700);
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s;
            touch-action: manipulation;
        }

        .footer-nav-btn:hover:not(:disabled) {
            background: var(--primary-light);
            color: var(--primary);
            border-color: var(--primary);
        }

        .footer-nav-btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        .footer-nav-info {
            font-size: 12px;
            font-weight: 700;
            color: var(--slate-500);
        }

        /* Floating Mobile Action Buttons */
        .mobile-fab-group {
            display: none;
            position: fixed;
            right: 16px;
            bottom: calc(16px + var(--safe-bottom));
            z-index: 850;
            flex-direction: column;
            gap: 10px;
            align-items: flex-end;
        }

        .fab-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            height: 44px;
            padding: 0 16px;
            background: var(--dark);
            color: #FFFFFF;
            border: none;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.3);
            touch-action: manipulation;
            transition: transform 0.15s, background-color 0.15s;
        }

        .fab-btn:active {
            transform: scale(0.96);
        }

        .fab-btn.primary {
            background: var(--primary);
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4);
        }

        .fab-top-btn {
            width: 44px;
            height: 44px;
            padding: 0;
            border-radius: 50%;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s, transform 0.2s;
        }

        .fab-top-btn.visible {
            opacity: 1;
            pointer-events: auto;
        }


        /* Responsive Breakpoints */
        @media (max-width: 992px) {
            body {
                flex-direction: column;
                padding-top: var(--mobile-nav-height);
            }

            .mobile-topbar {
                display: flex;
            }

            .sidebar {
                position: fixed;
                top: 0;
                left: 0;
                bottom: 0;
                width: min(340px, 86vw);
                height: 100vh;
                z-index: 1100;
                transform: translateX(-100%);
                box-shadow: 4px 0 24px rgba(0, 0, 0, 0.15);
            }

            .sidebar.open {
                transform: translateX(0);
            }

            .sidebar-backdrop {
                display: block;
            }

            .sidebar-close-btn {
                display: block;
            }

            .main-wrapper {
                padding: 20px 16px calc(60px + var(--safe-bottom));
                max-width: 100%;
            }

            .q-card {
                scroll-margin-top: calc(var(--mobile-nav-height) + 16px);
            }

            .mobile-fab-group {
                display: flex;
            }
        }

        @media (max-width: 640px) {
            .main-wrapper {
                padding: 12px 10px calc(70px + var(--safe-bottom));
            }

            .hero-banner {
                padding: 22px 16px;
                border-radius: 14px;
                margin-bottom: 20px;
            }

            .hero-banner h1 {
                font-size: 20px;
            }

            .hero-banner p {
                font-size: 13px;
                line-height: 1.5;
            }


            .q-card {
                border-radius: 12px;
                margin-bottom: 20px;
            }

            .q-header {
                padding: 14px 14px;
                flex-direction: column;
                gap: 8px;
            }

            .q-header h2 {
                font-size: 17px;
            }

            .q-tagline {
                font-size: 12.5px;
            }

            .tab-btn {
                padding: 8px 11px;
                font-size: 11.5px;
            }

            .tab-pane {
                padding: 14px 12px;
            }

            .change-box {
                padding: 12px 10px;
            }

            .diff-code {
                padding: 8px 10px;
                font-size: 11px;
            }

            pre.code-block {
                padding: 12px 10px;
                font-size: 11.5px;
                max-height: 380px;
            }

            .preview-frame {
                height: 360px;
            }

            .card-footer-nav {
                padding: 10px 12px;
            }

            .footer-nav-btn {
                padding: 7px 10px;
                font-size: 11px;
            }
        }
    </style>
</head>
<body>

    <!-- Sticky Mobile Topbar -->
    <header class="mobile-topbar" id="mobileTopbar">
        <div class="mobile-topbar-left">
            <button class="icon-btn" onclick="toggleSidebar(true)" aria-label="Open Navigation Menu">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="3" y1="12" x2="21" y2="12"></line>
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <line x1="3" y1="18" x2="21" y2="18"></line>
                </svg>
            </button>
            <div class="mobile-brand">
                <span>⚡ Solutions Hub</span>
                <span class="mobile-active-pill" id="mobileActiveQBadge">Q1</span>
            </div>
        </div>
    </header>

    <!-- Sidebar Backdrop for Mobile Drawer -->
    <div class="sidebar-backdrop" id="sidebarBackdrop" onclick="toggleSidebar(false)"></div>

    <!-- Sidebar Navigation Drawer -->
    <aside class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <div class="sidebar-header-info">
                <h1><span>⚡</span> Solutions Hub</h1>
                <p>29 Front-End Assessment Questions</p>
            </div>
            <button class="sidebar-close-btn" onclick="toggleSidebar(false)" aria-label="Close Navigation">✕</button>
        </div>

        <div class="sidebar-tools">
            <div class="sidebar-search-wrap">
                <input type="text" id="filterInput" placeholder="Filter questions..." oninput="filterQuestions()">
                <button class="clear-search-btn" id="clearSearchBtn" onclick="clearSearch()">✕</button>
            </div>
            <div class="filter-chips">
                <button class="chip-btn active" onclick="filterByRange('all', this)">All (29)</button>
                <button class="chip-btn" onclick="filterByRange('1-10', this)">Q1-Q10</button>
                <button class="chip-btn" onclick="filterByRange('11-20', this)">Q11-Q20</button>
                <button class="chip-btn" onclick="filterByRange('21-29', this)">Q21-Q29</button>
            </div>
        </div>

        <nav class="sidebar-menu" id="sidebarMenu">
'''

# Build sidebar items
for q in question_entries:
    html_output += f'''            <a href="#question-{q["num"]}" class="nav-item" id="nav-item-{q["num"]}" data-qnum="{q["num"]}" onclick="selectQuestion({q["num"]})">
                <span class="nav-badge">{q["num"]}</span>
                <span class="nav-title">{html.escape(q["title"])}</span>
            </a>\n'''

html_output += '''        </nav>
    </aside>

    <!-- Main Content -->
    <main class="main-wrapper">
        <!-- Hero Header -->
        <header class="hero-banner">
            <h1>Front-End Assessment: Verified Solutions</h1>
            <p>Complete corrected HTML, CSS, and JavaScript solutions for all 29 problems.</p>
        </header>
'''

# Build each Question Card
for q in question_entries:
    q_num = q["num"]
    esc_title = html.escape(q["title"])
    esc_badge = html.escape(q["badge"])
    esc_tagline = html.escape(q["tagline"])
    
    esc_h_target = html.escape(q["h_target"].strip())
    esc_h_repl = html.escape(q["h_repl"].strip())
    
    esc_c_target = html.escape(q["c_target"].strip())
    esc_c_repl = html.escape(q["c_repl"].strip())
    
    esc_j_target = html.escape(q["j_target"].strip())
    esc_j_repl = html.escape(q["j_repl"].strip())
    
    esc_solved_html = html.escape(q["solved_html"])
    esc_solved_css = html.escape(q["solved_css"])
    esc_solved_js = html.escape(q["solved_js"])
    
    # iframe srcdoc
    esc_demo_doc = html.escape(q["demo_doc"], quote=True)
    
    prev_disabled = 'disabled' if q_num == 1 else ''
    next_disabled = 'disabled' if q_num == 29 else ''
    prev_click = f'onclick="scrollToQuestion({q_num - 1})"' if q_num > 1 else ''
    next_click = f'onclick="scrollToQuestion({q_num + 1})"' if q_num < 29 else ''
    
    html_output += f'''
        <!-- Question {q_num}: {esc_title} -->
        <article class="q-card" id="question-{q_num}">
            <div class="q-header">
                <div class="q-title-group">
                    <div class="q-tags">
                        <span class="q-num">Q{q_num}</span>
                        <span class="q-badge">{esc_badge}</span>
                        <span class="q-verified-badge">✓ Solved</span>
                    </div>
                    <h2>{esc_title}</h2>
                    <p class="q-tagline">{esc_tagline}</p>
                </div>
            </div>

            <!-- Tabs Navigation -->
            <div class="tabs-bar">
                <button class="tab-btn active" onclick="switchTab(this, 'diff-{q_num}')">⚡ Changes</button>
                <button class="tab-btn" onclick="switchTab(this, 'html-{q_num}')">HTML</button>
                <button class="tab-btn" onclick="switchTab(this, 'css-{q_num}')">CSS</button>
                <button class="tab-btn" onclick="switchTab(this, 'js-{q_num}')">JavaScript</button>
                <button class="tab-btn" onclick="switchTab(this, 'live-{q_num}')">▶ Live Demo</button>
            </div>

            <!-- Tab 1: Diff / Changes -->
            <div class="tab-pane active" id="diff-{q_num}">
                <!-- HTML Change -->
                <div class="change-box html">
                    <h4><span>📄</span> HTML Modification</h4>
                    <div class="diff-view">
                        <div class="diff-item diff-before">
                            <div class="diff-label">Original / Starter Code</div>
                            <div class="diff-code">{esc_h_target}</div>
                        </div>
                        <div class="diff-item diff-after">
                            <div class="diff-label">Corrected Code</div>
                            <div class="diff-code">{esc_h_repl}</div>
                        </div>
                    </div>
                </div>

                <!-- CSS Change -->
                <div class="change-box css">
                    <h4><span>🎨</span> CSS Modification</h4>
                    <div class="diff-view">
                        <div class="diff-item diff-before">
                            <div class="diff-label">Original / Starter Code</div>
                            <div class="diff-code">{esc_c_target}</div>
                        </div>
                        <div class="diff-item diff-after">
                            <div class="diff-label">Corrected Code</div>
                            <div class="diff-code">{esc_c_repl}</div>
                        </div>
                    </div>
                </div>

                <!-- JS Change -->
                <div class="change-box js">
                    <h4><span>⚙️</span> JavaScript Logic Implementation</h4>
                    <div class="diff-view">
                        <div class="diff-item diff-before">
                            <div class="diff-label">Original / Starter Code</div>
                            <div class="diff-code">{esc_j_target}</div>
                        </div>
                        <div class="diff-item diff-after">
                            <div class="diff-label">Corrected Code</div>
                            <div class="diff-code">{esc_j_repl}</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tab 2: Full HTML -->
            <div class="tab-pane" id="html-{q_num}">
                <div class="code-container">
                    <div class="code-header">
                        <span>index.html</span>
                        <button class="copy-btn" onclick="copyCode(this)">Copy HTML</button>
                    </div>
                    <pre class="code-block"><code>{esc_solved_html}</code></pre>
                </div>
            </div>

            <!-- Tab 3: Full CSS -->
            <div class="tab-pane" id="css-{q_num}">
                <div class="code-container">
                    <div class="code-header">
                        <span>index.css</span>
                        <button class="copy-btn" onclick="copyCode(this)">Copy CSS</button>
                    </div>
                    <pre class="code-block"><code>{esc_solved_css}</code></pre>
                </div>
            </div>

            <!-- Tab 4: Full JS -->
            <div class="tab-pane" id="js-{q_num}">
                <div class="code-container">
                    <div class="code-header">
                        <span>index.js</span>
                        <button class="copy-btn" onclick="copyCode(this)">Copy JS</button>
                    </div>
                    <pre class="code-block"><code>{esc_solved_js}</code></pre>
                </div>
            </div>

            <!-- Tab 5: Live Interactive Demo -->
            <div class="tab-pane" id="live-{q_num}">
                <div class="preview-container">
                    <div class="preview-toolbar">
                        <span>Interactive Sandbox (Functional)</span>
                        <div class="preview-actions">
                            <button class="copy-btn" onclick="reloadIframe('frame-{q_num}')">↺ Reset</button>
                            <button class="copy-btn" onclick="openDemoFullscreen({q_num})">⛶ Fullscreen</button>
                        </div>
                    </div>
                    <iframe id="frame-{q_num}" class="preview-frame" srcdoc="{esc_demo_doc}" sandbox="allow-scripts"></iframe>
                </div>
            </div>

            <!-- Card Footer Navigation -->
            <div class="card-footer-nav">
                <button class="footer-nav-btn" {prev_click} {prev_disabled}>← Prev (Q{max(1, q_num - 1)})</button>
                <span class="footer-nav-info">Question {q_num} of 29</span>
                <button class="footer-nav-btn" {next_click} {next_disabled}>Next (Q{min(29, q_num + 1)}) →</button>
            </div>
        </article>
'''

html_output += '''
    </main>

    <!-- Floating Action Buttons for Mobile -->
    <div class="mobile-fab-group">
        <button class="fab-btn fab-top-btn" id="fabTopBtn" onclick="scrollToTop()" aria-label="Scroll to top" title="Scroll to top">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="19" x2="12" y2="5"></line>
                <polyline points="5 12 12 5 19 12"></polyline>
            </svg>
        </button>
        <button class="fab-btn primary" onclick="toggleSidebar(true)" aria-label="Questions list" title="Browse Questions">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="8" y1="6" x2="21" y2="6"></line>
                <line x1="8" y1="12" x2="21" y2="12"></line>
                <line x1="8" y1="18" x2="21" y2="18"></line>
                <line x1="3" y1="6" x2="3.01" y2="6"></line>
                <line x1="3" y1="12" x2="3.01" y2="12"></line>
                <line x1="3" y1="18" x2="3.01" y2="18"></line>
            </svg>
            <span>Questions (29)</span>
        </button>
    </div>


    <script>
        // Tab switching
        function switchTab(btn, paneId) {
            var card = btn.closest('.q-card');
            var buttons = card.querySelectorAll('.tab-btn');
            var panes = card.querySelectorAll('.tab-pane');
            
            for (var i = 0; i < buttons.length; i++) {
                buttons[i].classList.remove('active');
            }
            for (var j = 0; j < panes.length; j++) {
                panes[j].classList.remove('active');
            }
            
            btn.classList.add('active');
            var targetPane = document.getElementById(paneId);
            if (targetPane) {
                targetPane.classList.add('active');
            }
        }

        // Copy code to clipboard with touch vibration
        function copyCode(btn) {
            var container = btn.closest('.code-container');
            var code = container.querySelector('code').textContent;
            navigator.clipboard.writeText(code).then(function() {
                if (navigator.vibrate) navigator.vibrate(40);
                var origText = btn.textContent;
                btn.textContent = '✓ Copied!';
                btn.style.background = '#10B981';
                setTimeout(function() {
                    btn.textContent = origText;
                    btn.style.background = '';
                }, 2000);
            }).catch(function(err) {
                alert('Copy failed: ' + err);
            });
        }

        // Reload iframe demo
        function reloadIframe(frameId) {
            var frame = document.getElementById(frameId);
            if (frame) {
                var doc = frame.getAttribute('srcdoc');
                frame.srcdoc = doc;
            }
        }

        // Open live interactive demo in full tab/window (great for mobile touch testing)
        function openDemoFullscreen(qNum) {
            var frame = document.getElementById('frame-' + qNum);
            if (!frame) return;
            var docHtml = frame.getAttribute('srcdoc');
            var blob = new Blob([docHtml], { type: 'text/html;charset=utf-8' });
            var url = URL.createObjectURL(blob);
            window.open(url, '_blank');
        }

        // Mobile drawer toggle
        function toggleSidebar(forceOpen) {
            var sidebar = document.getElementById('sidebar');
            var backdrop = document.getElementById('sidebarBackdrop');
            if (!sidebar || !backdrop) return;
            
            var isOpen = typeof forceOpen === 'boolean' ? forceOpen : !sidebar.classList.contains('open');
            if (isOpen) {
                sidebar.classList.add('open');
                backdrop.classList.add('active');
                document.body.style.overflow = 'hidden'; // prevent background scrolling on mobile
            } else {
                sidebar.classList.remove('open');
                backdrop.classList.remove('active');
                document.body.style.overflow = '';
            }
        }

        // Select question from sidebar
        function selectQuestion(qNum) {
            toggleSidebar(false);
            scrollToQuestion(qNum);
        }

        // Smooth scroll to question card
        function scrollToQuestion(qNum) {
            var card = document.getElementById('question-' + qNum);
            if (card) {
                card.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }

        // Scroll to top
        function scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Search / filter sidebar
        function filterQuestions() {
            var input = document.getElementById('filterInput');
            var clearBtn = document.getElementById('clearSearchBtn');
            var filter = input.value.toLowerCase().trim();
            
            if (clearBtn) {
                clearBtn.style.display = filter ? 'block' : 'none';
            }

            var items = document.querySelectorAll('.nav-item');
            for (var i = 0; i < items.length; i++) {
                var text = items[i].textContent.toLowerCase();
                if (!filter || text.indexOf(filter) !== -1) {
                    items[i].style.display = 'flex';
                } else {
                    items[i].style.display = 'none';
                }
            }
        }

        function clearSearch() {
            var input = document.getElementById('filterInput');
            input.value = '';
            filterQuestions();
            input.focus();
        }

        // Filter chips (All, Q1-10, Q11-20, Q21-29)
        function filterByRange(range, chipBtn) {
            var chips = document.querySelectorAll('.chip-btn');
            chips.forEach(function(c) { c.classList.remove('active'); });
            chipBtn.classList.add('active');

            var items = document.querySelectorAll('.nav-item');
            items.forEach(function(item) {
                var qnum = parseInt(item.getAttribute('data-qnum'), 10);
                var match = true;
                if (range === '1-10') match = qnum >= 1 && qnum <= 10;
                else if (range === '11-20') match = qnum >= 11 && qnum <= 20;
                else if (range === '21-29') match = qnum >= 21 && qnum <= 29;
                item.style.display = match ? 'flex' : 'none';
            });
        }

        // Active scroll spy for both Desktop sidebar and Mobile header
        var scrollTimeout;
        window.addEventListener('scroll', function() {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(function() {
                var cards = document.querySelectorAll('.q-card');
                var scrollPos = window.scrollY + 120;
                var currentQ = 'Q1';
                
                for (var i = 0; i < cards.length; i++) {
                    var card = cards[i];
                    var top = card.offsetTop;
                    var height = card.offsetHeight;
                    var num = card.getAttribute('id').replace('question-', '');
                    var navItem = document.getElementById('nav-item-' + num);
                    
                    if (scrollPos >= top && scrollPos < top + height) {
                        currentQ = 'Q' + num;
                        if (navItem) navItem.classList.add('active');
                    } else {
                        if (navItem) navItem.classList.remove('active');
                    }
                }
                
                var mobileBadge = document.getElementById('mobileActiveQBadge');
                if (mobileBadge) mobileBadge.textContent = currentQ;

                var fabTop = document.getElementById('fabTopBtn');
                if (fabTop) {
                    if (window.scrollY > 300) {
                        fabTop.classList.add('visible');
                    } else {
                        fabTop.classList.remove('visible');
                    }
                }
            }, 30);
        });

        // Touch swipe-left to close sidebar drawer on mobile
        var touchStartX = 0;
        var touchStartY = 0;
        var sidebarEl = document.getElementById('sidebar');
        if (sidebarEl) {
            sidebarEl.addEventListener('touchstart', function(e) {
                touchStartX = e.changedTouches[0].screenX;
                touchStartY = e.changedTouches[0].screenY;
            }, { passive: true });

            sidebarEl.addEventListener('touchend', function(e) {
                var diffX = e.changedTouches[0].screenX - touchStartX;
                var diffY = e.changedTouches[0].screenY - touchStartY;
                if (diffX < -50 && Math.abs(diffX) > Math.abs(diffY)) {
                    toggleSidebar(false);
                }
            }, { passive: true });
        }

    </script>
</body>
</html>
'''

with open('answer.html', 'w', encoding='utf-8') as out_f:
    out_f.write(html_output)

print(f"Generated answer.html successfully! File size: {len(html_output)} bytes.")
