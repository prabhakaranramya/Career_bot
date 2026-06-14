from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np

TRAINING_DATA = [
    ("I just graduated and looking for my first job", "entry_level"),
    ("I have no experience but want to start coding", "entry_level"),
    ("I am a fresh graduate in computer science", "entry_level"),
    ("I want to switch careers completely", "career_switch"),
    ("I have 5 years experience but want to move to data science", "career_switch"),
    ("I am currently a teacher and want to move into tech", "career_switch"),
    ("I have 2 years of experience and want to grow", "mid_level"),
    ("I am a junior developer looking to become senior", "mid_level"),
    ("I want to get promoted and take on more responsibility", "mid_level"),
    ("I am a senior engineer and want to move into management", "senior_level"),
    ("I have 10 years experience and considering leadership", "senior_level"),
    ("I want to start my own company", "senior_level"),
]

texts  = [t for t, _ in TRAINING_DATA]
labels = [l for _, l in TRAINING_DATA]

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("clf",   MultinomialNB()),
])
pipeline.fit(texts, labels)

STAGE_LABELS = {
    "entry_level":   "🌱 Entry Level",
    "career_switch": "🔄 Career Switcher",
    "mid_level":     "📈 Mid-Level",
    "senior_level":  "🏆 Senior / Leadership",
}

def classify_career_stage(text: str) -> dict:
    prediction = pipeline.predict([text])[0]
    confidence = round(float(np.max(pipeline.predict_proba([text])[0])) * 100, 1)
    return {"stage": prediction, "label": STAGE_LABELS.get(prediction), "confidence": confidence}