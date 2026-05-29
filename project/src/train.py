import pandas as pd
import pickle
import re
import os

os.makedirs('artifacts', exist_ok=True)

df = pd.read_csv('data/raw/IMDB_Dataset.csv')
df['sentiment'] = df['sentiment'].map({'positive': 1, 'negative': 0})

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

df['clean_review'] = df['review'].apply(clean_text)
X = df['clean_review']
y = df['sentiment']

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

vectorizer = TfidfVectorizer(max_features=5000)
X_tfidf = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_tfidf, y)

# Сохраняем
with open('artifacts/model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('artifacts/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("Модель и векторизатор сохранены в artifacts/")
