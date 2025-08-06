from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

# Load the menu
with open("menu.json", "r") as f:
    menu = json.load(f)

@app.route("/")
def home():
    return "✅ Food Bidding Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"reply": "Invalid request!"}), 400

        user_message = data["message"].lower()
        bid_match = re.search(r"(?:order|want|give me|get)\s+([\w\s]+?)\s+(?:for|at)\s+(\d+)", user_message)

        if bid_match:
            item_name = bid_match.group(1).strip()
            bid_price = int(bid_match.group(2))

            # Match item from menu (case-insensitive)
            matched_item = next((item for item in menu if item["name"].lower() == item_name), None)

            if matched_item:
                if bid_price >= matched_item["min_price"]:
                    response = f"✅ Bid Accepted for {matched_item['name']} at ₹{bid_price}!"
                else:
                    response = f"❌ Bid too low. Minimum price for {matched_item['name']} is ₹{matched_item['min_price']}."
            else:
                response = "😕 Sorry, that item is not on the menu."

        else:
            response = "👋 Welcome to the Food Bidding Bot! Try something like: 'I want oreo shake for 70'"
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "⚠️ An error occurred processing your request."}), 500

        return jsonify({"reply": response}), 200

    

if __name__ == "__main__":
   app.run(debug=True, host="0.0.0.0", port=5000)
