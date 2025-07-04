from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            count = 0
            if os.path.exists('count.json'):
                with open('count.json', 'r') as file:
                    data = json.load(file)
                    count = data.get('count', 0)
            
            count += 1
            
            with open('count.json', 'w') as file:
                json.dump({'count': count}, file)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'count': count}).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
