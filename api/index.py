from http.server import BaseHTTPRequestHandler
from pythainlp import word_tokenize
from pythainlp.transliterate import romanize
import json

def handler(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            thai_text = body.get('text', '')
            
            words = word_tokenize(thai_text, engine="newmm")
            result = []
            for word in words:
                result.append({
                    "word": word,
                    "tlit": romanize(word),
                    "chinese": ""
                })
            
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "status": "success",
                    "words": result
                })
            }
            
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "status": "error",
                    "message": str(e)
                })
            }
    
    return {
        "statusCode": 200,
        "body": "Thai Tokenizer API"
    }
