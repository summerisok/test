import os
from pythainlp import word_tokenize

# 设置 PyThaiNLP 数据目录为 /tmp 目录
os.environ["PYTHAINLP_DATA_DIR"] = "/tmp"

# 然后正常处理其他逻辑
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 检查是否请求了 /favicon.png，如果是，则返回404
            if self.path == '/favicon.png':
                self.send_response(404)
                self.end_headers()
                return

            # 获取请求中的查询参数
            from urllib.parse import urlparse, parse_qs
            query_components = parse_qs(urlparse(self.path).query)
            thai_text = query_components.get('text', None)

            if not thai_text:
                # 如果未提供文本，返回400 Bad Request
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

            # 输出响应
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            # 捕获所有异常，返回500错误，并记录异常信息
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            error_message = {
                'error': 'Internal Server Error',
                'message': str(e)  # 显示具体的异常信息
            }

            # 输出错误消息
            self.wfile.write(json.dumps(error_message, ensure_ascii=False).encode('utf-8'))
