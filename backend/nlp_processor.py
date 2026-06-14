import spacy
import nltk
from nltk.tokenize import word_tokenize

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None

SKILL_KEYWORDS = {
    "programming": ["python", "javascript", "java", "c++", "typescript", "golang"],
    "data":        ["machine learning", "data science", "pandas", "sql", "tensorflow", "nlp"],
    "web":         ["react", "html", "css", "node", "django", "flask", "angular"],
    "cloud":       ["aws", "azure", "gcp", "docker", "kubernetes", "devops"],
    "design":      ["figma", "ui", "ux", "photoshop", "illustrator"],
    "soft_skills": ["leadership", "communication", "management", "agile", "scrum"],
}

INTENT_PATTERNS = {
    "career_switch":   ["switch", "change career", "move into", "transition", "new field"],
    "skill_gap":       ["learn", "improve", "upskill", "skill", "course", "certif"],
    "job_search":      ["job", "interview", "resume", "cv", "apply", "hiring", "salary"],
    "career_growth":   ["promote", "promotion", "senior", "advance", "grow", "raise"],
    "roadmap_request": ["roadmap", "plan", "guide", "path", "steps", "how to become"],
    "general":         [],
}

def extract_intent_and_skills(text: str):
    text_lower = text.lower()

    detected_intent = "general"
    for intent, keywords in INTENT_PATTERNS.items():
        if any(kw in text_lower for kw in keywords):
            detected_intent = intent
            break

    detected_skills = []
    for category, skills in SKILL_KEYWORDS.items():
        for skill in skills:
            if skill in text_lower:
                detected_skills.append(skill)

    if nlp:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT"]:
                detected_skills.append(ent.text.lower())

    return detected_intent, list(set(detected_skills))