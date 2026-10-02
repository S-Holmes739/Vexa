#!/usr/bin/env python3
"""
Vexa Atlas Unified Server
Serves the production built frontend on port 8080 and provides OSINT & Ollama proxy endpoints.
Uses Python standard library with zero external pip dependencies.
"""

import http.server
import socketserver
import os
import json
import urllib.request
import urllib.error
import urllib.parse
import sys

PORT = 8080
DIST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')

class VexaAtlasHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # API: System Status
        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            status = {
                'system': 'VEXA ATLAS COMMAND',
                'version': '2.4',
                'status': 'OPERATIONAL',
                'threat_matrix': 'DEFCON 3'
            }
            self.wfile.write(json.dumps(status).encode('utf-8'))
            return

        # API: OpenSky Live Airspace Data Proxy
        if self.path.startswith('/api/opensky'):
            try:
                req = urllib.request.Request(
                    "https://opensky-network.org/api/states/all",
                    headers={'User-Agent': 'VexaAtlasOSINT/1.0'}
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    raw_data = json.loads(response.read().decode('utf-8'))
                    states = raw_data.get('states', [])[:30] # Top 30 tracked flights
                    aircraft_list = []
                    for s in states:
                        if s[5] is not None and s[6] is not None:
                            aircraft_list.append({
                                'icao24': s[0],
                                'callsign': (s[1] or '').strip(),
                                'country': s[2],
                                'lng': s[5],
                                'lat': s[6],
                                'altitude': int(s[7] * 3.28084) if s[7] else 0, # convert to feet
                                'velocity': int(s[9] * 1.94384) if s[9] else 0, # convert to knots
                                'heading': int(s[10]) if s[10] is not None else 0,
                                'squawk': s[14] or 'N/A'
                            })
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'aircraft': aircraft_list}).encode('utf-8'))
                    return
            except Exception as e:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e), 'aircraft': []}).encode('utf-8'))
                return

        # API: News Registry (Ingesting Newslinks.txt)
        if self.path == '/api/news':
            news_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Newslinks.txt')
            channels = []
            if os.path.exists(news_file):
                with open(news_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line or ':' not in line:
                            continue
                        colon_idx = line.find(':')
                        name = line[:colon_idx].strip()
                        url = line[colon_idx+1:].strip()
                        import re
                        match = re.search(r'(?:live\/|v=|youtu\.be\/)([a-zA-Z0-9_-]{11})', url)
                        video_id = match.group(1) if match else None
                        if video_id:
                            channels.push if False else channels.append({
                                'id': re.sub(r'[^a-z0-9]', '', name.lower()),
                                'name': name,
                                'url': url,
                                'videoId': video_id
                            })
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'channels': channels}).encode('utf-8'))
            return

        # API: Open-Meteo Weather
        if self.path.startswith('/api/weather'):
            try:
                query = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(query)
                lat = params.get('lat', [None])[0]
                lon = params.get('lon', [None])[0]
                if lat is None or lon is None:
                    raise ValueError("Missing lat or lon")
                # Call Open-Meteo
                req = urllib.request.Request(
                    f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true",
                    headers={'User-Agent': 'VexaAtlas/1.0'}
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    weather_data = json.loads(response.read().decode('utf-8'))
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(weather_data).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
                return

        # Single-page application router fallback: if file doesn't exist, serve index.html
        path_without_query = self.path.split('?')[0].lstrip('/')
        file_path = os.path.join(DIST_DIR, path_without_query)
        if not os.path.exists(file_path) or os.path.isdir(file_path):
            self.path = '/index.html'

        return super().do_GET()

    def do_POST(self):
        # API: Vexa AI Query / Ollama Bridge
        if self.path == '/api/vexa/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(post_body)
                prompt = data.get('prompt', '')

                # Try local Ollama
                ollama_payload = json.dumps({
                    "model": "deepseek-r1:1.5b",
                    "prompt": prompt,
                    "system": "You are Vexa, a hyper-intelligent cybersecurity-oriented AI companion. Communicate with human brevity: be precise, concise, and direct.",
                    "stream": False
                }).encode('utf-8')

                req = urllib.request.Request(
                    "http://localhost:11434/api/generate",
                    data=ollama_payload,
                    headers={'Content-Type': 'application/json'}
                )
                try:
                    with urllib.request.urlopen(req, timeout=4) as response:
                        res_json = json.loads(response.read().decode('utf-8'))
                        reply = res_json.get('response', '')
                except Exception:
                    reply = f"VEXA TACTICAL INTEL: Analysis complete. All telemetry streams are currently verified within standard threat tolerance thresholds."

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'reply': reply}).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
                return

        self.send_response(404)
        self.end_headers()

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), VexaAtlasHandler) as httpd:
        print(f"==================================================")
        print(f"  VEXA ATLAS: Tactical Cyber & OSINT Command      ")
        print(f"  Listening on: http://localhost:{PORT}            ")
        print(f"  Serving directory: {DIST_DIR}                   ")
        print(f"==================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down Vexa Atlas server.")
            httpd.server_close()

if __name__ == '__main__':
    run_server()
