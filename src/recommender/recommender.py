import pandas as pd
from src.nlp.semantic_search import semantic_search

df = pd.read_csv("data/processed/final_data.csv")


def recommend(user, query):

    results = df.copy()

    # -------------------------
    # FILTERING
    # -------------------------
    results = results[
        (results["age_min"] <= user["age"]) &
        (results["age_max"] >= user["age"])
    ]

    results = results[
        (results["gender"] == user["gender"]) |
        (results["gender"] == "all")
    ]

    results = results[
        results["income_max"] >= user["income"]
    ]

    results = results[
        (results["occupation"] == user["occupation"]) |
        (results["occupation"] == "all")
    ]

    results = results[
        (results["state"] == user["state"]) |
        (results["state"] == "all")
    ]

    print("After filtering:", results.shape)

    # -------------------------
    # EMBEDDING SEARCH
    # -------------------------
    final_results = semantic_search(query, results)

    return final_results