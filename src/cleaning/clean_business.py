import pandas as pd


def clean_business_data():
    # Load raw file
    df = pd.read_csv("data/raw/business_women_schemes.csv")

    # -----------------------------
    # Standardize column names
    # -----------------------------
    df.columns = [col.strip().lower() for col in df.columns]

    # -----------------------------
    # Rename to match final schema
    # -----------------------------
    df = df.rename(columns={
        "scheme": "scheme_name",
        "name": "scheme_name",
        "income": "income_max"
    })

    # -----------------------------
    # Add missing columns (VERY IMPORTANT)
    # -----------------------------
    required_cols = [
        "age_min", "state", "income_max", "ministry",
        "scheme_type", "benefits", "category",
        "description", "eligibility", "scheme_name"
    ]

    for col in required_cols:
        if col not in df.columns:
            df[col] = "all"   # default value

    # -----------------------------
    # Fix category for business women
    # -----------------------------
    df["category"] = "business women"
    # -----------------------------
    # Clean text columns
    # -----------------------------
    df["scheme_name"] = df["scheme_name"].astype(str).str.strip()
    df["description"] = df["description"].astype(str).str.lower()

    # -----------------------------
    # Save cleaned file
    # -----------------------------
    output_path = "data/interim/cleaned_business.csv"
    df.to_csv(output_path, index=False)

    print(f"✅ Cleaned business dataset saved at: {output_path}")


if __name__ == "__main__":
    clean_business_data()