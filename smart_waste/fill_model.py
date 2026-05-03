import pandas as pd
from sklearn.linear_model import LinearRegression

def train_model():
    data = pd.read_csv("dataset/fill_data.csv")

    X = data[["Day"]]
    y = data["Fill_Level"]

    model = LinearRegression()
    model.fit(X, y)
    return model

model = train_model()

def predict_fill(day):
    return model.predict([[day]])[0]

def predict_full_day():
    for d in range(1, 20):
        if predict_fill(d) >= 100:
            return d
    return "Not reached"