from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        message = "Hello from Python on Vercel!"
        self.wfile.write(json.dumps({"message": message}).encode())
        return
