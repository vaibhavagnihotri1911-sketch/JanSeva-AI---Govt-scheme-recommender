from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load model once when the application starts
model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_search(query, df):

    # Combine scheme name and description
    texts = (
        df["scheme_name"].fillna("")
        + " "
        + df["description"].fillna("")
    ).tolist()

    # Create embeddings for schemes
    scheme_embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    # Create embedding for user query
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    # Calculate cosine similarity
    scores = cosine_similarity(
        query_embedding,
        scheme_embeddings
    )[0]

    # Add scores
    df = df.copy()
    df["score"] = scores

    # Sort by relevance
    df = df.sort_values(
        by="score",
        ascending=False
    )

    return df
