from http.server import BaseHTTPRequestHandler
import json
from .thai_dict import THAI_DICT  # 导入字典
import oss2  # 阿里云 OSS SDK

# OSS配置
auth = oss2.Auth('<AccessKeyId>', '<AccessKeySecret>')
bucket = oss2.Bucket(auth, 'oss-cn-beijing.aliyuncs.com', '<your-bucket-name>')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        # 获取音频文件URL
        audio_url = bucket.sign_url('GET', 'audio/sawadee.mp3', 3600)  # 1小时有效期
        
        self.wfile.write(json.dumps({
            "message": "Audio URL generated",
            "url": audio_url
        }).encode())
        return

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
