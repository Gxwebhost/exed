from http.server import BaseHTTPRequestHandler
import json
import os
from vercel_blob import BlobStore

blob = BlobStore(token=os.environ.get('BLOB_READ_WRITE_TOKEN'))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            data = blob.get('counter.json')
            current_count = json.loads(data).get('count', 0) if data else 0
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'count': current_count}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_POST(self):
        try:
            data = blob.get('counter.json')
            current_count = json.loads(data).get('count', 0) if data else 0
            new_count = current_count + 1
            
            blob.put('counter.json', json.dumps({'count': new_count}), {
                'contentType': 'application/json'
            })
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'count': new_count}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
