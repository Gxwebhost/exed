from http.server import BaseHTTPRequestHandler
import json
from vercel_blob import put, get

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            count_data = get('counter.json').json()
            current_count = count_data.get('count', 0)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'count': current_count}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def do_POST(self):
        try:
            try:
                count_data = get('counter.json').json()
                current_count = count_data.get('count', 0)
            except:
                current_count = 0
                
            new_count = current_count + 1
            put('counter.json', json.dumps({'count': new_count}), {
                'contentType': 'application/json'
            })
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'count': new_count}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
