from sentence_transformers import SentenceTransformer, util

model = None  # Startup pe load mat karo!

def get_model():
    global model
    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

def semantic_search(query, df):
    m = get_model()
    texts = df["scheme_name"].fillna("") + " " + df["description"].fillna("")
    scheme_embeddings = m.encode(texts.tolist(), convert_to_tensor=True)
    query_embedding = m.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, scheme_embeddings)[0]
    df = df.copy()
    df["score"] = scores.cpu().numpy()
    df = df.sort_values(by="score", ascending=False)
    return df
