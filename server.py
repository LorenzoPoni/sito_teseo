import http.server
import json
import socketserver
from urllib.parse import urlparse

PORT = 3000
latest_reasoning = "In attesa di dati da Mind+..."

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        global latest_reasoning
        
        if self.path == '/api/ai-reasoning':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                latest_reasoning = data.get('reasoning') or data.get('message') or json.dumps(data)
                print(f"Ricevuto da Mind+: {latest_reasoning}")
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success', 'received': latest_reasoning}).encode())
            except Exception as e:
                print(f"Errore parsing JSON: {e}")
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        global latest_reasoning
        
        if self.path == '/api/ai-reasoning':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'reasoning': latest_reasoning}).encode())
        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server in esecuzione su http://localhost:{PORT}")
    print(f"Mind+ puo inviare dati a: http://localhost:{PORT}/api/ai-reasoning")
    print("Premi Ctrl+C per fermare il server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer fermato.")
