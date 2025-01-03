from pythainlp import word_tokenize
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 获取请求中的查询参数 (假设参数名为 'text')
        from urllib.parse import urlparse, parse_qs
        query_components = parse_qs(urlparse(self.path).query)
        thai_text = query_components.get('text', None)

        if not thai_text:
            # 没有提供文本时返回400 Bad Request
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Please provide text to tokenize in Thai.')
            return

        # 泰语分词
        segmented_text = word_tokenize(thai_text[0], engine='newmm')

        # 生成JSON响应
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = {
            'original_text': thai_text[0],
            'segmented_text': segmented_text
        }
        import json
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
