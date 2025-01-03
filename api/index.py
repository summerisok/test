from http.server import BaseHTTPRequestHandler
import json
from pythainlp import word_tokenize
from pythainlp.transliterate import romanize

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        message = "Thai Tokenizer API is working!"
        self.wfile.write(json.dumps({"message": message}).encode())
        return

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            thai_text = data.get('text', '')
            
            # 泰语分词
            words = word_tokenize(thai_text, engine="newmm")
            result = []
            
            # 处理每个词
            for word in words:
                result.append({
                    "word": word,
                    "tlit": romanize(word),  # 添加罗马音转写
                    "chinese": ""  # 预留中文翻译字段
                })
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "words": result
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "error",
                "message": str(e)
            }).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
