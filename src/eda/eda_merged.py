import pandas as pd

# Load merged dataset
df = pd.read_csv("data/processed/merged_data.csv")

print("Dataset Shape:", df.shape)
print("\nColumns:\n", df.columns)
# BASIC INFO
print("\nInfo:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())
# CATEGORY DISTRIBUTION
print("\nTop Categories:")
print(df["category"].value_counts().head(10))
# TARGET GROUP
print("\nTarget Groups:")
print(df["target_group"].value_counts().head(10))
# STATE DISTRIBUTION
print("\nTop States:")
print(df["state"].value_counts().head(10))
# INCOME ANALYSIS
if "income_max" in df.columns:
    print("\nIncome Stats:")
    print(df["income_max"].describe())
# AGE RANGE
if "age_min" in df.columns:
    print("\nAge Range:")
    print("Min age:", df["age_min"].min())
    print("Max age:", df["age_max"].max())