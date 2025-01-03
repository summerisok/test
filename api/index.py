from http.server import BaseHTTPRequestHandler
import json

# 简单的泰语分词函数
def simple_thai_tokenize(text):
    # 泰语字符范围
    thai_chars = '\u0E00-\u0E7F'
    
    words = []
    current_word = ''
    
    for char in text:
        if any(ord(c) in range(0x0E00, 0x0E7F + 1) for c in char):
            current_word += char
        else:
            if current_word:
                words.append(current_word)
                current_word = ''
            if not char.isspace():
                words.append(char)
    
    if current_word:
        words.append(current_word)
    
    return words

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "success",
            "message": "Thai Tokenizer API is working"
        }).encode('utf-8'))

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            thai_text = data.get('text', '')
            
            # 使用简单分词
            words = simple_thai_tokenize(thai_text)
            result = []
            
            for word in words:
                result.append({
                    "word": word,
                    "tlit": "",  # 暂时不做罗马音转换
                    "chinese": ""
                })
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "words": result
            }).encode('utf-8'))
            
        except Exception as e:
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
