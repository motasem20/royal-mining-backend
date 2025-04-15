# Flask Backend with MongoDB (for Royal Mining Game)

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://rapuser:motasem0776622174@royalmining.iyszgb2.mongodb.net/?retryWrites=true&w=majority&appName=royalmining"
client = MongoClient(MONGO_URI)
db = client["royal_mining"]
collection = db["users"]

@app.route("/save", methods=["POST"])
def save_user():
    data = request.json
    user_id = data.get("wallet_id") or data.get("telegram_id")
    if not user_id:
        return jsonify({"error": "No user ID provided"}), 400

    # Store all relevant data
    user_data = {
        "wallet_id": data.get("wallet_id"),
        "telegram_id": data.get("telegram_id"),
        "score": data.get("score", 0),
        "exp": data.get("exp", 0),
        "level": data.get("level", 1),
        "rank": data.get("rank", "مبتدئ"),
        "multiplier": data.get("multiplier", 1),
    }

    query = {"$or": [
        {"wallet_id": data.get("wallet_id")},
        {"telegram_id": data.get("telegram_id")}
    ]}

    collection.update_one(query, {"$set": user_data}, upsert=True)
    return jsonify({"message": "User data saved"})

@app.route("/load", methods=["GET"])
def load_user():
    wallet_id = request.args.get("wallet_id")
    telegram_id = request.args.get("telegram_id")

    if not wallet_id and not telegram_id:
        return jsonify({"error": "No ID provided"}), 400

    query = {"$or": [
        {"wallet_id": wallet_id},
        {"telegram_id": telegram_id}
    ]}

    user = collection.find_one(query, {"_id": 0})
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
