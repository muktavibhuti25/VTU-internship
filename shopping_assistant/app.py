from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

# Load dataset
data = pd.read_csv("dataset.csv")

# Try loading recommendation files (if created)
try:
    similarity = pickle.load(open("similarity.pkl", "rb"))
    data_model = pickle.load(open("data.pkl", "rb"))
except:
    similarity = None
    data_model = None


# 🔹 Home page
@app.route("/")
def home():
    return render_template("chat.html")


# 🔹 Recommendation function
def recommend(product_name):
    if similarity is None or data_model is None:
        return ["⚠ Recommendation system not available"]

    product_name = product_name.lower()

    matches = data_model[data_model["name"].str.lower().str.contains(product_name)]

    if matches.empty:
        return ["❌ Product not found"]

    idx = matches.index[0]

    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]

    results = []
    for i in scores:
        product = data_model.iloc[i[0]]
        results.append(f"{product['name']} - ₹{product['price']} ⭐{product['rating']}")

    return results


# 🔹 Chat API
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"].lower()

    # 🔥 Recommendation query
    if "recommend" in user_input:
        product_name = user_input.replace("recommend", "").strip()
        recs = recommend(product_name)

        return jsonify({
            "reply": "🤖 Recommended Products:\n\n" + "\n".join(recs)
        })

    # 🔍 Dynamic search (ALL PRODUCTS)
    results = data[
        data["name"].str.lower().str.contains(user_input, na=False) |
        data["category"].str.lower().str.contains(user_input, na=False)
    ]

    # 💰 Price filter (example: "under 20000")
    if "under" in user_input:
        try:
            price = int(user_input.split("under")[1].strip())
            results = results[results["price"] <= price]
        except:
            pass

    # ⭐ Sort by rating
    results = results.sort_values(by="rating", ascending=False)

    # ❌ No results
    if results.empty:
        return jsonify({"reply": "❌ No matching products found."})

    # ✅ Show top results
    response = "🛒 Top Products:\n\n"

    for _, row in results.head(5).iterrows():
        response += f"{row['name']}\n₹{row['price']} ⭐{row['rating']}\n\n"

    return jsonify({"reply": response})


# 🔹 Run app
if __name__ == "__main__":
    app.run(debug=True)