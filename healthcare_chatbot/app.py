from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
data = pd.read_csv("dataset.csv")

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]

    input_vector = vectorizer.transform([user_input])
    prediction = model.predict(input_vector)[0]

    precautions = data[data["disease"] == prediction]["precautions"].values[0]

    return jsonify({
        "reply": f"Disease: {prediction}\nPrecautions: {precautions}"
    })

if __name__ == "__main__":
    app.run(debug=True)