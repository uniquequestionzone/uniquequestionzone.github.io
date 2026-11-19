"""
Launcher for 'PUBG: Cottage Battle Royale'.
Runs a local server and launches the default web browser.
"""
import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket

def find_free_port(start_port=8000):
    port = start_port
    while port < 8100:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
        port += 1
    return 8000

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'

def run_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    port = find_free_port()
    server_address = ('0.0.0.0', port)
    local_ip = get_local_ip()
    
    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

    httpd = HTTPServer(server_address, QuietHandler)
    url_local = f"http://127.0.0.1:{port}/index.html"
    url_mobile = f"http://{local_ip}:{port}/index.html"
    
    print("=" * 65)
    print("      PUBG: COTTAGE BATTLE ROYALE (3D HOUSE ROYALE)")
    print("            [Mobile Friendly & Desktop Edition]")
    print("=" * 65)
    print(f"  PC Browser URL   : {url_local}")
    print(f"  Mobile Phone URL : {url_mobile}")
    print("  (Connect phone to same Wi-Fi & open the Mobile URL above)")
    print("-" * 65)
    print("  CONTROLS (DESKTOP):")
    print("    - W, A, S, D / Arrows : Move & Climb Ladder")
    print("    - Left Click          : Fire (Auto Spray / Sniper Shot)")
    print("    - Right Click         : ADS / Sniper Scope Zoom")
    print("    - R                   : Reload Weapon")
    print("    - 1 / 2               : Switch Weapon (M416 / AWM Sniper)")
    print("    - H                   : Quick Full Heal")
    print("    - Shift               : Sprint")
    print("    - Space               : Jump & Auto Step-Up")
    print("    - E                   : Open / Close Front Door")
    print("    - V                   : Toggle 1st & 3rd Person View")
    print("    - X                   : Toggle Recon ESP Vision")
    print("-" * 65)
    print("  CONTROLS (MOBILE & TABLET):")
    print("    - Left Virtual Joystick : Move & Climb Ladder")
    print("    - Right Screen Drag     : Aim & Look Around")
    print("    - Big Red Button        : Shoot (Hold to Spray / Tap)")
    print("    - Action Buttons        : Scope, Jump, Reload, Heal, Switch, Door")
    print("=" * 65)
    print("  Press Ctrl+C in this terminal to stop the game server.")
    print("=" * 65)

    webbrowser.open(url_local)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nGame server stopped.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
