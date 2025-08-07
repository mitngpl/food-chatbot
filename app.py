from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

# Load menu
with open("menu.json", "r") as f:
    menu = json.load(f)

@app.route("/")
def home():
    return "✅ Food Bidding Bot is live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("Received:", data)

        if not data or "message" not in data:
            return jsonify({"reply": "❌ Invalid message format"}), 400

        message = data["message"].lower()
        print("User message:", message)

        # Try to extract food item and price
        match = re.search(r"(\w+(?:\s+\w+)*)\s+for\s+(\d+)", message)
        if not match:
            return jsonify({"reply": "❌ Could not understand your bid. Try 'cheese pizza for 90'."})

        item = match.group(1).strip().lower()
        offered_price = int(match.group(2))

        # Check menu for item
        matched_item = None
        for menu_item in menu["items"]:
            if item in menu_item["name"].lower():
                matched_item = menu_item
                break

        if not matched_item:
            return jsonify({"reply": f"❌ Sorry, we don't have '{item}' on the menu."})

        actual_price = matched_item["price"]
        if offered_price >= actual_price:
            return jsonify({"reply": f"✅ Deal! Your order for {matched_item['name']} at ₹{offered_price} is confirmed."})
        else:
            return jsonify({"reply": f"❌ Sorry, ₹{offered_price} is too low for {matched_item['name']}. Actual price is ₹{actual_price}."})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"reply": "❌ Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
