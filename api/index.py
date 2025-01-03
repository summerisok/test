from fastapi import FastAPI
from pythainlp import word_tokenize
from pythainlp.transliterate import romanize
from pydantic import BaseModel

app = FastAPI()

class ThaiText(BaseModel):
    text: str

@app.post("/api/tokenize")
async def tokenize(thai_text: ThaiText):
    try:
        words = word_tokenize(thai_text.text, engine="newmm")
        result = []
        for word in words:
            result.append({
                "word": word,
                "tlit": romanize(word),
                "chinese": ""
            })
        
        return {
            "status": "success",
            "words": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/api")
async def root():
    return {"message": "Thai Tokenizer API"}
