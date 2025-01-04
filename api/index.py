from http.server import BaseHTTPRequestHandler
import json
import re

def thai_tokenize(text):
    # 定义泰语词典
    thai_dict = {
        'สวัสดี': 'sawadee',
        'ครับ': 'khrap',
        'ค่ะ': 'kha',
        'ขอบคุณ': 'khobkhun',
        'ผม': 'phom',
        'ดิฉัน': 'dichan',
        'ชื่อ': 'chue',
        'อยู่': 'yuu',
        'ไป': 'pai',
        'มา': 'ma'
    }
    
    # 找到最长匹配的词
    result = []
    while text:
        longest_match = ''
        for word in thai_dict:
            if text.startswith(word) and len(word) > len(longest_match):
                longest_match = word
        
        if longest_match:
            result.append({
                'word': longest_match,
                'tlit': thai_dict[longest_match]
            })
            text = text[len(longest_match):]
        else:
            # 如果没有匹配到词典中的词，取第一个字符
            result.append({
                'word': text[0],
                'tlit': ''
            })
            text = text[1:]
    
    return result

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
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "words": words
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
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
