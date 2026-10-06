from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI
from dotenv import load_dotenv
import os

# LOAD ENV VARIABLES
load_dotenv()

app = Flask(__name__)

# DATABASE CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# OPENAI CLIENT
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------- DATABASE MODEL ----------------
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)

# CREATE DATABASE
with app.app_context():
    db.create_all()

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- CHAT API ----------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"reply": "No message received"}), 400

    user_message = data["message"]

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=user_message
        )

        ai_reply = response.output_text

        # SAVE TO DATABASE
        chat_data = Chat(
            user_message=user_message,
            ai_response=ai_reply
        )

        db.session.add(chat_data)
        db.session.commit()

        return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"reply": str(e)})

# ---------------- CHAT HISTORY ----------------
@app.route("/history")
def history():
    chats = Chat.query.all()

    data = [
        {"user": chat.user_message, "ai": chat.ai_response}
        for chat in chats
    ]

    return jsonify(data)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)