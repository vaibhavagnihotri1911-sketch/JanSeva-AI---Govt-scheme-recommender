import pandas as pd

print("🔄 Loading cleaned datasets...")

# Load cleaned datasets
df1 = pd.read_csv("data/interim/cleaned_gov.csv")
df2 = pd.read_csv("data/interim/cleaned_kaggle.csv")
df3 = pd.read_csv("data/interim/cleaned_business.csv")

print("GOV shape:", df1.shape)
print("Kaggle shape:", df2.shape)
print("Business Women Schemes shape:", df3.shape)

# -------------------------------
# STEP 1: Standardize column names
# -------------------------------
df1.columns = df1.columns.str.lower().str.strip()
df2.columns = df2.columns.str.lower().str.strip()
df3.columns = df3.columns.str.lower().str.strip()



# -------------------------------
# STEP 2: Get all unique columns
# -------------------------------
all_columns = list(set(df1.columns).union(set(df2.columns).union(set(df3.columns))))

# -------------------------------
# STEP 3: Add missing columns to both datasets
# -------------------------------
for col in all_columns:
    if col not in df1.columns:
        df1[col] = "Not Available"
    if col not in df2.columns:
        df2[col] = "Not Available"
    if col not in df3.columns:
        df3[col] = "Not Available"

# Reorder columns (important for clean merge)
df1 = df1[all_columns]
df2 = df2[all_columns]
df3 = df3[all_columns]


# -------------------------------
# STEP 4: Merge datasets
# -------------------------------
df = pd.concat([df1, df2, df3], ignore_index=True)

if "scheme_name" not in df.columns:
    df["scheme_name"] = df["benefits"]

print("After merge shape:", df.shape)

# -------------------------------
# STEP 5: Remove duplicates
# -------------------------------
df = df.drop_duplicates()

print("After removing duplicates:", df.shape)

# -------------------------------
# STEP 6: Fill missing values
# -------------------------------
df.fillna("Not Available", inplace=True)

# -------------------------------
# STEP 7: Save merged dataset
# -------------------------------
output_path = "data/processed/merged_data.csv"
df.to_csv(output_path, index=False)

print(f"✅ Merged dataset saved at: {output_path}")