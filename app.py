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
        print("Incoming data:", data)

        user_msg = data.get("message", "").lower()

        # Match menu item and price from user's message
        for item, price in menu.items():
            if item in user_msg:
                match = re.search(r"\b(\d+)\b", user_msg)
                if match:
                    offered_price = int(match.group(1))
                    if offered_price >= price:
                        response = f"✅ Order confirmed for {item} at ₹{offered_price}!"
                    else:
                        response = f"❌ Sorry, ₹{offered_price} is too low for {item}. Actual price is ₹{price}."
                else:
                    response = f"🧾 Price for {item} is ₹{price}. How much would you like to bid?"

                return jsonify({"reply": response})

        return jsonify({"reply": "❓ Sorry, I couldn't understand your order. Please mention item and price."})

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "❌ Internal server error"}), 500

if __name__ == "__main__":
   app.run(debug=True, host="0.0.0.0", port=5000)
