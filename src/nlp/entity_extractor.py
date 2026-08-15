import re

def extract_entities(text):
    text = text.lower()
    
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

    # Age: pehle "age <number>" ya "<number> saal/years/yrs" jaisa context dhoondo
    age_match = re.search(r'(?:age\s*|umar\s*)(\d{1,3})|(\d{1,3})\s*(?:saal|years?|yrs?)', text)
    if age_match:
        age_str = age_match.group(1) or age_match.group(2)
        age = int(age_str)
        if 0 < age < 120:
            user["age"] = age

    return user

if __name__ == "__main__":
    print(extract_entities("i am a poor student from delhi age 21"))
