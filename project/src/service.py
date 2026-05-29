from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.model import SentimentModel
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sentiment Analysis API")

model = SentimentModel()

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    sentiment: str
    confidence: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Empty text")
    sentiment, confidence = model.predict(request.text)
    logger.info(f"Request: {request.text[:50]}... -> {sentiment} ({confidence:.2f})")
    return PredictResponse(sentiment=sentiment, confidence=confidence)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
