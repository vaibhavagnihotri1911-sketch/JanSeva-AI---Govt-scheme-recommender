import pandas as pd

df = pd.read_csv("data/raw/gov_schemes.csv", on_bad_lines='skip',engine='python')

print("Before cleaning:", df.shape)

df = df.drop_duplicates()
df.columns = df.columns.str.lower().str.strip()

df.fillna({
    "gender": "All",
    "occupation": "All",
    "state": "All",
    "family_income_max": 500000
}, inplace=True)

print("After cleaning:", df.shape)

df.to_csv("data/interim/cleaned_gov.csv", index=False)

print("✅ GOV cleaned")