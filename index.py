from http.server import BaseHTTPRequestHandler
from api.translate import handler

def handle(req):
    return handler(req)

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        return handle(self)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
