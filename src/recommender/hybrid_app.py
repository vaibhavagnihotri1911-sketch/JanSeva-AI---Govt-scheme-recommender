from src.nlp.speech_input import get_voice_input
from src.nlp.text_processing import normalize_text
from src.nlp.entity_extractor import extract_entities
from src.recommender.recommender import recommend

print("🚀 AI Scheme Recommender (Voice + NLP + Embeddings)")

mode = input("\nChoose input (text/voice): ").lower()

# INPUT
if mode == "voice":
    raw_text = get_voice_input()
else:
    raw_text = input("Enter your query: ")

print("\n🗣 Raw:", raw_text)

# TEXT PROCESSING
clean_text = normalize_text(raw_text)

print("🔤 Clean:", clean_text)

# NLP EXTRACTION
user = extract_entities(clean_text)

print("\n🧠 User Profile:", user)

# FINAL RECOMMENDATION
results = recommend(user, clean_text)

print("\n🎯 Recommended Schemes:\n")
print(results[["scheme_name", "category", "benefits"]])