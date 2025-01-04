from http.server import BaseHTTPRequestHandler
import json

# 泰语词典
THAI_DICT = {
    'สวัสดี': 'sawadee',    # hello
    'ครับ': 'khrap',       # polite particle (male)
    'ค่ะ': 'kha',         # polite particle (female)
    'ขอบคุณ': 'khobkhun',  # thank you
    'ชื่อ': 'chue',        # name
    'ผม': 'phom',         # I (male)
    'ดิฉัน': 'dichan',     # I (female)
    'เป็น': 'pen',        # to be
    'อยู่': 'yuu',        # to stay
    'ไป': 'pai',         # to go
    'มา': 'ma',          # to come
}

def thai_tokenize(text):
    words = []
    while text:
        # 找到最长匹配的词
        found = False
        for word in sorted(THAI_DICT.keys(), key=len, reverse=True):
            if text.startswith(word):
                words.append({
                    'word': word,
                    'tlit': THAI_DICT[word]
                })
                text = text[len(word):]
                found = True
                break
        
        # 如果没找到匹配的词，取第一个字符
        if not found:
            words.append({
                'word': text[0],
                'tlit': ''
            })
            text = text[1:]
    
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
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        thai_text = data.get('text', '')
        
        # 进行分词
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
