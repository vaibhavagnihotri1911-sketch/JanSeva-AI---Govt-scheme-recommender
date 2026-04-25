import pandas as pd

print("Loading merged dataset...")

# Load data
df = pd.read_csv("data/processed/merged_data.csv")

print("Initial shape:", df.shape)

# 1. CLEAN NUMERIC COLUMNS
print("\nConverting numeric columns...")

# Income
if "income_max" in df.columns:
    df["income_max"] = pd.to_numeric(df["income_max"], errors='coerce')
    print("Missing income before:", df["income_max"].isnull().sum())

    df["income_max"] = df["income_max"].fillna(df["income_max"].median())

    print("Income dtype:", df["income_max"].dtype)

# Age
if "age_min" in df.columns:
    df["age_min"] = pd.to_numeric(df["age_min"], errors='coerce')
    df["age_min"] = df["age_min"].fillna(0)

if "age_max" in df.columns:
    df["age_max"] = pd.to_numeric(df["age_max"], errors='coerce')
    df["age_max"] = df["age_max"].fillna(100)

# 2. STANDARDIZE TEXT
print("\nCleaning text columns...")

text_cols = ["gender", "occupation", "state", "category"]

for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.lower().str.strip()

# 3. CREATE FEATURES
print("\n Creating new features...")

# Age group
if "age_min" in df.columns:
    df["age_group"] = pd.cut(
        df["age_min"],
        bins=[0, 18, 35, 60, 100],
        labels=["child", "youth", "adult", "senior"]
    )

# Income group
if "income_max" in df.columns:
    df["income_group"] = pd.cut(
        df["income_max"],
        bins=[0, 200000, 500000, 1000000, 10000000],
        labels=["low", "middle", "upper_middle", "high"]
    )


# 4. NLP FEATURE
print("\nCreating combined text feature...")

df["combined_text"] = (
    df.get("scheme_name", "").astype(str) + " " +
    df.get("category", "").astype(str) + " " +
    df.get("description", "").astype(str) + " " +
    df.get("benefits", "").astype(str) + " " +
    df.get("target_group", "").astype(str)
)

# 5. HANDLE MISSING VALUES (FIXED)
print("\nHandling missing values...")

# Only fill text columns (avoid categorical error)
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].fillna("not available")

# 6. FINAL CHECK
print("\nFinal shape:", df.shape)

print("\nSample data:")
print(df.head(3))

# 7. SAVE FINAL DATA
output_path = "data/processed/final_data.csv"
df.to_csv(output_path, index=False)

print(f"\nFeature engineering completed!")
print(f"Saved at: {output_path}")