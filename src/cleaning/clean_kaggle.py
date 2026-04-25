import pandas as pd

df = pd.read_csv("data/raw/kaggle_cleaned.csv")

print("Before cleaning:", df.shape)

df = df.drop_duplicates()
df.columns = df.columns.str.lower().str.strip()

df.fillna({
    "gender": "All",
    "occupation": "All",
    "state": "All"
}, inplace=True)

print("After cleaning:", df.shape)

df.to_csv("data/interim/cleaned_kaggle.csv", index=False)

print("✅ Kaggle dataset cleaned and saved!")