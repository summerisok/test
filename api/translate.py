from http.server import BaseHTTPRequestHandler
from pythainlp import word_tokenize
from pythainlp.transliterate import romanize
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 读取请求内容
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        # 获取泰语文本
        thai_text = data.get('text', '')
        
        try:
            # 分词处理
            words = word_tokenize(thai_text, engine="newmm")
            result = []
            for word in words:
                result.append({
                    "word": word,
                    "tlit": romanize(word),
                    "chinese": ""
                })
            
            # 返回成功结果
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "words": result
            }).encode('utf-8'))
            
        except Exception as e:
            # 返回错误信息
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "error",
                "message": str(e)
            }).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()