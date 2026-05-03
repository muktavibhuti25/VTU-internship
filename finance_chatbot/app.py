from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

app = Flask(__name__)

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount INTEGER,
            category TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------- CHART ----------
def generate_chart():
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()

    if df.empty:
        return

    category_sum = df.groupby('category')['amount'].sum()

    if os.path.exists("static/chart.png"):
        os.remove("static/chart.png")

    plt.figure()
    category_sum.plot(kind='bar')
    plt.title("Expenses by Category")
    plt.savefig("static/chart.png")
    plt.close()

# ---------- RECOMMENDATION ----------
def generate_recommendations():
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()

    if df.empty:
        return "No data available. Add expenses first."

    total = df['amount'].sum()
    category_sum = df.groupby('category')['amount'].sum()

    msg = ""

    # Alerts
    if total > 5000:
        msg += "⚠️ Alert: Spending exceeded ₹5000!\n"

    if total > 10000:
        msg += "🚨 Critical: Budget limit crossed!\n"

    max_category = category_sum.idxmax()
    max_value = category_sum.max()

    if max_value > 2000:
        msg += f"⚠️ High spending on {max_category} (₹{max_value})\n"

    # Daily alert
    today = datetime.now().strftime("%Y-%m-%d")
    daily_total = df[df['date'] == today]['amount'].sum()

    if daily_total > 2000:
        msg += "⚠️ High spending today!\n"

    # Suggestions
    msg += "\n💡 Recommendations:\n"
    msg += "- Follow 50-30-20 rule\n"
    msg += "- Save at least 20% income\n"
    msg += "- Reduce unnecessary expenses\n"

    return msg

# ---------- CHATBOT ----------
def chatbot_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input:
        return "Hello! I'm your Finance Assistant 💰"

    elif "add" in user_input:
        try:
            parts = user_input.split()
            amount = int(parts[1])
            category = parts[2] if len(parts) > 2 else "general"

            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
                      (amount, category, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()

            return f"Added ₹{amount} under {category}"
        except:
            return "Use format: add 500 food"

    elif "total" in user_input:
        conn = sqlite3.connect('database.db')
        df = pd.read_sql_query("SELECT * FROM expenses", conn)
        conn.close()
        return f"Total spending: ₹{df['amount'].sum()}"

    elif "chart" in user_input:
        generate_chart()
        return "Chart generated! 📊"

    elif "recommend" in user_input or "suggest" in user_input:
        return generate_recommendations()

    elif "bye" in user_input:
        return "Goodbye! Stay financially smart 💰"

    else:
        return "Try: add 500 food | total | chart | recommend"

# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_response():
    msg = request.form["msg"]
    return jsonify(chatbot_response(msg))

if __name__ == "__main__":
    app.run(debug=True)