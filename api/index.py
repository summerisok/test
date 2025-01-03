from http.server import BaseHTTPRequestHandler
import json

def thai_tokenize(text):
    # 简单的泰语分词函数
    words = []
    current_word = ''
    
    for char in text:
        if ord(char) >= 0x0E00 and ord(char) <= 0x0E7F:  # 泰语字符范围
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
            
            # 使用自定义分词函数
            words = thai_tokenize(thai_text)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "words": words
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "error",
                "message": str(e)
            }).encode())
