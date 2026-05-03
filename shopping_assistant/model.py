import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
data = pd.read_csv("dataset.csv")

# Combine text features
data["features"] = data["category"] + " " + data["description"]

# Convert to vectors
vectorizer = TfidfVectorizer()
feature_matrix = vectorizer.fit_transform(data["features"])

# Similarity matrix
similarity = cosine_similarity(feature_matrix)

# Save files
pickle.dump(similarity, open("similarity.pkl", "wb"))
pickle.dump(data, open("data.pkl", "wb"))

print("Model + Recommendation system ready!")