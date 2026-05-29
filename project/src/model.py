import pickle
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH", "artifacts/model.pkl")
VECTORIZER_PATH = os.getenv("VECTORIZER_PATH", "artifacts/vectorizer.pkl")

class SentimentModel:
    def __init__(self):
        with open(MODEL_PATH, 'rb') as f:
            self.model = pickle.load(f)
        with open(VECTORIZER_PATH, 'rb') as f:
            self.vectorizer = pickle.load(f)

    def predict(self, text: str):
        import re
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        vec = self.vectorizer.transform([text])
        proba = self.model.predict_proba(vec)[0]
        pred = self.model.predict(vec)[0]
        sentiment = "positive" if pred == 1 else "negative"
        confidence = max(proba)
        return sentiment, confidence