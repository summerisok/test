from http.server import BaseHTTPRequestHandler
import json
import sys
import traceback

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "message": "API is working"
            }).encode('utf-8'))
        except Exception as e:
            self.send_error_response(e)

    def do_POST(self):
        try:
            # 读取请求内容
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            thai_text = data.get('text', '')
            
            # 简单的分词处理
            words = [thai_text]  # 暂时返回原文
            result = []
            
            for word in words:
                result.append({
                    "word": word,
                    "tlit": "",
                    "chinese": ""
                })
            
            # 返回结果
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "words": result,
                "debug": sys.version  # 添加 Python 版本信息
            }).encode('utf-8'))
            
        except Exception as e:
            self.send_error_response(e)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def send_error_response(self, error):
        self.send_response(500)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "error",
            "message": str(error),
            "traceback": traceback.format_exc()
        }).encode('utf-8'))
