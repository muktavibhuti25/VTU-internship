import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

data = pd.read_csv("dataset.csv")

X = data["symptoms"]
y = data["disease"]

vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

model = RandomForestClassifier()
model.fit(X_vectorized, y)

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained!")