import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from src.model import SentimentModel

def test_model_loads():
    model = SentimentModel()
    assert model.model is not None
    assert model.vectorizer is not None

def test_predict_positive():
    model = SentimentModel()
    sent, conf = model.predict("I love this movie, it's amazing!")
    assert sent == "positive"
    assert 0.5 <= conf <= 1.0

def test_predict_negative():
    model = SentimentModel()
    sent, conf = model.predict("Terrible, worst film ever.")
    assert sent == "negative"
    assert 0.5 <= conf <= 1.0