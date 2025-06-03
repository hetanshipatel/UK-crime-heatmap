import pandas as pd
import ast

df = pd.read_csv("data/uk_crime_data.csv")

# Convert 'location' column from stringified dict to real dict
df["location"] = df["location"].apply(ast.literal_eval)

# Extract latitude and longitude
df["latitude"] = df["location"].apply(lambda x: x.get("latitude") if isinstance(x, dict) else None)
df["longitude"] = df["location"].apply(lambda x: x.get("longitude") if isinstance(x, dict) else None)

# Keep selected columns
columns_to_keep = ["city", "category", "location_type", "latitude", "longitude", "month"]
df_cleaned = df[columns_to_keep].copy()

df_cleaned.rename(columns={
    "category": "crime_type"
}, inplace=True)

# Drop rows with missing coordinates
df_cleaned.dropna(subset=["latitude", "longitude"], inplace=True)

df_cleaned.to_csv("data/uk_crime_cleaned.csv", index=False)

print(f"✅ Cleaned data saved to 'data/uk_crime_cleaned.csv'")
print(f"📊 Cleaned rows: {len(df_cleaned)}")
print(f"🧹 Unique crime types: {df_cleaned['crime_type'].nunique()}")
