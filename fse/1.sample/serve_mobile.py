#!/usr/bin/env python3
"""
Mobile Access Server for answer.html
-----------------------------------
Starts a local web server, detects your Wi-Fi/LAN IP address, prints a scannable
terminal QR code, and allows seamless mobile phone access to answer.html.
"""

import sys
import os
import socket
import io
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False


def get_local_ip():
    """Detect the local LAN / Wi-Fi IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Does not actually send packets, just finds the outbound interface IP
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def find_free_port(start_port=8000, max_attempts=20):
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port
            except OSError:
                continue
    return start_port


class MobileServerHandler(SimpleHTTPRequestHandler):
    """Custom request handler with root redirect and dynamic QR image support."""

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Redirect root '/' to '/answer.html'
        if path == '/' or path == '':
            self.send_response(302)
            self.send_header('Location', '/answer.html')
            self.end_headers()
            return

        # Dynamic QR code endpoint: /qr.png?data=...
        if path == '/qr.png':
            query = urllib.parse.parse_qs(parsed.query)
            data = query.get('data', [f'http://{self.server.local_ip}:{self.server.server_port}/answer.html'])[0]
            
            if HAS_QRCODE:
                img = qrcode.make(data)
                buf = io.BytesIO()
                img.save(buf, format='PNG')
                png_bytes = buf.getvalue()
                
                self.send_response(200)
                self.send_header('Content-Type', 'image/png')
                self.send_header('Content-Length', str(len(png_bytes)))
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                self.wfile.write(png_bytes)
                return
            else:
                self.send_response(404)
                self.end_headers()
                return

        # Server info JSON endpoint: /api/info
        if path == '/api/info':
            import json
            info = {
                'ip': self.server.local_ip,
                'port': self.server.server_port,
                'url': f'http://{self.server.local_ip}:{self.server.server_port}/answer.html'
            }
            body = json.dumps(info).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # Standard file serving
        return super().do_GET()

    def end_headers(self):
        # Enable CORS and caching headers for smooth mobile browsing
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()


def print_banner(ip, port):
    url = f"http://{ip}:{port}/answer.html"
    local_url = f"http://localhost:{port}/answer.html"

    print("=" * 64)
    print(" 🚀 MOBILE ACCESS SERVER FOR ANSWER.HTML")
    print("=" * 64)
    print()
    print("  📱 Mobile Phone URL (Ensure phone is on same Wi-Fi):")
    print(f"     👉 \033[1;32m{url}\033[0m")
    print()
    print("  💻 Desktop Local URL:")
    print(f"     👉 \033[1;36m{local_url}\033[0m")
    print()

    if HAS_QRCODE:
        print("  📷 SCAN THIS QR CODE WITH YOUR MOBILE CAMERA TO OPEN:")
        print("-" * 64)
        try:
            qr = qrcode.QRCode(box_size=1, border=2)
            qr.add_data(url)
            qr.print_ascii(invert=True)
        except Exception:
            try:
                qr = qrcode.QRCode(box_size=1, border=1)
                qr.add_data(url)
                qr.print_ascii(invert=False)
            except Exception as e:
                print(f"     (Could not display ASCII QR: {e})")
        print("-" * 64)
    else:
        print("  Tip: Run 'pip install qrcode' for terminal QR code support.")

    print()
    print("  ✨ Press Ctrl + C to stop the server.")
    print("=" * 64)
    print()


def run_server():
    # Change working directory to the directory of this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    local_ip = get_local_ip()
    port = find_free_port(8000)

    server = HTTPServer(('0.0.0.0', port), MobileServerHandler)
    server.local_ip = local_ip
    server.server_port = port

    print_banner(local_ip, port)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped gracefully.")
        server.server_close()


if __name__ == '__main__':
    run_server()
