import spacy
import re

nlp = None  # Lazy load

def get_nlp():
    global nlp
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")
    return nlp

def extract_entities(text):
    nlp_model = get_nlp()
    text = text.lower()
    doc = nlp_model(text)
    
    user = {
        "age": 25,
        "gender": "all",
        "income": 500000,
        "occupation": "all",
        "state": "all",
        "category": "general"
    }

    if any(word in text for word in ["student", "btech", "college"]):
        user["occupation"] = "student"
    elif any(word in text for word in ["farmer", "kisan", "agriculture"]):
        user["occupation"] = "farmer"
    elif any(word in text for word in ["business", "entrepreneur", "startup"]):
        user["occupation"] = "business"

    if any(word in text for word in ["female", "mahila", "woman", "ladki"]):
        user["gender"] = "female"
    elif any(word in text for word in ["male", "man"]):
        user["gender"] = "male"

    if any(word in text for word in ["student", "scholarship", "education"]):
        user["category"] = "student"
    elif any(word in text for word in ["farmer", "kisan"]):
        user["category"] = "farmer"
    elif any(word in text for word in ["health", "insurance"]):
        user["category"] = "health"
    elif any(word in text for word in ["sc", "st"]):
        user["category"] = "sc/st"
    elif any(word in text for word in ["widow", "pension"]):
        user["category"] = "widow"
    elif any(word in text for word in ["old", "senior", "elderly"]):
        user["category"] = "senior"
    elif any(word in text for word in ["woman", "female", "mahila"]):
        user["category"] = "women"

    if any(word in text for word in ["poor", "low income", "garib"]):
        user["income"] = 200000

    age_match = re.search(r'\b\d{1,3}\b', text)
    if age_match:
        age = int(age_match.group())
        if 0 < age < 120:
            user["age"] = age

    return user

if __name__ == "__main__":
    print(extract_entities("i am a poor student from delhi age 21"))
