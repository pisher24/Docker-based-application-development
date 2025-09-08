from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# load .env if present
load_dotenv()

app = Flask(__name__)
CORS(app)  # allow cross-origin from frontend

# Get Mongo URI from env var; default to local Mongo for dev
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")  # in docker-compose we'll run mongo optionally
client = MongoClient(MONGO_URI)
db = client.get_database(os.getenv("MONGO_DB", "todo_db"))
collection = db.get_collection(os.getenv("MONGO_COLLECTION", "items"))

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    data = request.get_json() or {}
    item_name = data.get("itemName")
    item_description = data.get("itemDescription")

    if not item_name or not item_description:
        return jsonify({"error": "itemName and itemDescription are required"}), 400

    doc = {
        "itemName": item_name,
        "itemDescription": item_description
    }
    result = collection.insert_one(doc)
    return jsonify({"message": "To-Do item submitted successfully", "id": str(result.inserted_id)}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
