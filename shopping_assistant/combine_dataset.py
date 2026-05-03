import pandas as pd

# Load dataset
df = pd.read_csv("C:/Users/Mukta Vibhuti/Downloads/archive/flipkart_sales_enriched.csv")

print("Columns:", df.columns)

# Rename columns CORRECTLY based on your dataset
df = df.rename(columns={
    "Product Name": "name",
    "Category": "category",
    "Price (INR)": "price",
    "Customer Rating": "rating"
})

# Add description (not available in your dataset)
df["description"] = df["category"]

# Clean price (already numeric but safe)
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Remove missing values
df = df.dropna()

# Keep only required columns
df = df[["name", "category", "price", "rating", "description"]]

# Save final dataset
df.to_csv("dataset.csv", index=False)

print("✅ Dataset ready for project!")