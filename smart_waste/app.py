from flask import Flask, render_template, request
import os
import pandas as pd

# Import your models
from waste_model import predict_waste   # or from predict import predict_waste (for CNN)
from fill_model import predict_fill, predict_full_day

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    waste_type = None
    fill_prediction = None
    full_day = None
    alert = None

    # Load dataset for graph
    data = pd.read_csv("dataset/fill_data.csv")
    days = data["Day"].tolist()
    levels = data["Fill_Level"].tolist()

    if request.method == "POST":
        file = request.files["image"]

        if file:
            # Save uploaded image
            path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(path)

            # Waste prediction
            waste_type = predict_waste(path)

            # Fill level prediction (example: current day = 5)
            fill_prediction = round(predict_fill(5), 2)

            # Predict when bin is full
            full_day = predict_full_day()

            # 🔔 Alert logic
            if isinstance(full_day, int) and full_day <= 6:
                alert = "⚠️ Bin will be full soon! Schedule pickup."

    return render_template(
        "index.html",
        waste_type=waste_type,
        fill_prediction=fill_prediction,
        full_day=full_day,
        alert=alert,
        days=days,
        levels=levels
    )


if __name__ == "__main__":
    app.run(debug=True)