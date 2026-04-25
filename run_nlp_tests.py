from src.nlp.text_processing import normalize_text
from src.nlp.entity_extractor import extract_entities
from src.nlp.semantic_search import semantic_search
import pandas as pd


# -----------------------------
# INTENT DETECTION (same logic)
# -----------------------------
def detect_intent(user, text):
    text = text.lower()

    # priority: extracted category
    if user.get("category") != "general":
        return user["category"]

    if any(word in text for word in ["scholarship", "education", "study"]):
        return "student"

    elif any(word in text for word in ["farmer", "kisan"]):
        return "farmer"

    elif any(word in text for word in ["health", "medical", "hospital", "treatment"]):
        return "health"

    elif any(word in text for word in ["widow", "pension"]):
        return "widow"

    elif any(word in text for word in ["business", "loan", "startup"]):
        if user.get("gender") == "female":
            return "business_women"
        return "business"

    elif any(word in text for word in ["woman", "female", "mahila"]):
        return "women"

    elif any(word in text for word in ["old", "senior"]):
        return "senior"

    return "general"


# -----------------------------
# STRICT FILTER (same logic)
# -----------------------------
def apply_strict_filter(df, intent):
    print(f"\nDetected Intent: {intent}\n")

    if intent == "student":
        return df[df["category"].str.contains("student|education|scholarship", case=False, na=False)]

    elif intent == "farmer":
        return df[df["category"].str.contains("farmer|agriculture", case=False, na=False)]

    elif intent == "business":
        return df[
            df["category"].str.contains("business|startup|entrepreneur|loan|msme", case=False, na=False)
        ]

    elif intent == "business_women":
        return df[
            df["scheme_name"].str.contains(
                "mudra|udyogini|stand up|pmegp|mahila", case=False, na=False
            )
            |
            df["category"].str.contains(
                "business|entrepreneur|women", case=False, na=False
            )
        ]

    elif intent == "women":
        return df[df["category"].str.contains("women|female", case=False, na=False)]

    elif intent == "widow":
        return df[df["category"].str.contains("widow|pension", case=False, na=False)]

    elif intent == "senior":
        return df[df["category"].str.contains("senior|old|pension", case=False, na=False)]

    elif intent == "health":
        return df[
            df["category"].str.contains("health|insurance|medical", case=False, na=False)
        ]

    return df


# -----------------------------
# QUERY EXPANSION (same logic)
# -----------------------------
SYNONYMS = {
    "student": ["student", "education", "scholarship", "study", "college"],
    "business": ["business", "loan", "startup", "msme", "entrepreneur", "self employment"],
    "farmer": ["farmer", "kisan", "agriculture", "crop"],
    "women": ["women", "mahila", "female", "girl"],
    "widow": ["widow", "pension", "destitute"],
    "senior": ["senior", "old", "elderly", "pension"],
    "health": ["health", "medical", "hospital", "insurance"]
}


def expand_query(text, intent):
    expanded = text.lower()

    if intent in SYNONYMS:
        expanded += " " + " ".join(SYNONYMS[intent])

    return expanded


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def run_tests():
    print("Running NLP Tests...\n")

    # CHANGE INPUT HERE
    #text = "I belong to a poor family and i want help for my health issues for all"
    #text = "I am a student looking for scholarship"
    #text = "I am a farmer seeking government schemes"
    text = "I am a woman entrepreneur looking for business loans"
    #text = "I am a widow looking for pension schemes"
    #text = "I am a senior citizen looking for old age pension"
    #text = "I am a girl/women student looking for education schemes"
    #text = "I am student want to go abroad or foreign for higher studies but I am from a poor family and I need financial help"
    #text = "I belong to a poor family and i want help for my health issues for all"

    # Step 1: Clean text
    clean, _ = normalize_text(text)
    print("Clean Text:", clean)

    # Step 2: Load dataset
    df = pd.read_csv("data/processed/final_data.csv")

    # Step 3: Extract user info
    user = extract_entities(clean)
    print("User Info:", user)

    # Step 4: Detect intent
    intent = detect_intent(user, clean)
    print("Final Intent:", intent)

    # Step 5: Apply filter
    filtered_df = apply_strict_filter(df, intent)

    if len(filtered_df) == 0:
        print("No strict match -> using full dataset")
        filtered_df = df.copy()

    print("Rows after strict filtering:", len(filtered_df))

    # Step 6: Semantic search
    expanded_query = expand_query(clean, intent)
    results = semantic_search(expanded_query, filtered_df)

    print("Raw results:", len(results))

    # Step 7: Confidence filter
    if "score" in results.columns:
        results = results[results["score"] > 0.3]

    print("After score filter:", len(results))

    # Final output
    print("\nRecommended Schemes:\n")

    if len(results) == 0:
        print("No schemes found.")
    else:
        print(results[["scheme_name", "category", "score"]].head(5))


# -----------------------------
# RUN FILE
# -----------------------------
if __name__ == "__main__":
    run_tests()