from http.server import BaseHTTPRequestHandler
import json
from .thai_dict import THAI_DICT  # 导入字典

def thai_tokenize(text):
    words = []
    while text:
        # 找到最长匹配的词
        found = False
        for word in sorted(THAI_DICT.keys(), key=len, reverse=True):
            if text.startswith(word):
                word_info = THAI_DICT[word].copy()
                word_info['word'] = word
                words.append(word_info)
                text = text[len(word):]
                found = True
                break
        
        if not found:
            words.append({
                'word': text[0],
                'tlit': '',
                'chinese': ''
            })
            text = text[1:]
    
    return words

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        message = "Thai Dictionary API is working!"
        self.wfile.write(json.dumps({"message": message}).encode())
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        thai_text = data.get('text', '')
        tokens = thai_tokenize(thai_text)
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "success",
            "words": tokens
        }
        self.wfile.write(json.dumps(response).encode())
        return
