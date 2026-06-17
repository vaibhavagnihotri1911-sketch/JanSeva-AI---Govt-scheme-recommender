from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def semantic_search(query, df):
    texts = (
        df["scheme_name"].fillna("") 
        + " " 
        + df["description"].fillna("")
    )

    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform(texts.tolist() + [query])

    query_vector = vectors[-1]
    scheme_vectors = vectors[:-1]

    scores = cosine_similarity(
        query_vector,
        scheme_vectors
    )[0]

    df = df.copy()
    df["score"] = scores

    df = df.sort_values(
        by="score",
        ascending=False
    )

    return df
