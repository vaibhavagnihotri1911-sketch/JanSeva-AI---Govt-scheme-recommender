from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_search(query, df):

    texts = df["scheme_name"].fillna("") + " " + df["description"].fillna("")

    scheme_embeddings = model.encode(texts.tolist(), convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, scheme_embeddings)[0]

    df = df.copy()   # FIX
    df["score"] = scores.cpu().numpy()

    # SORT BY SCORE
    df = df.sort_values(by="score", ascending=False)

    return df