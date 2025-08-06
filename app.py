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

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        response = "Sorry, I didn’t understand that."

        for item, price in menu.items():
            if item in user_message:
                # Extract user's offered price
                import re
                match = re.search(r'(\d+)', user_message)
                if match:
                    offered_price = int(match.group(1))
                    if offered_price >= price:
                        response = f"✅ Order confirmed for {item} at ₹{offered_price}!"
                    else:
                        response = f"❌ Sorry, we can't accept ₹{offered_price} for {item}. Actual price is ₹{price}."
                else:
                    response = f"The price for {item} is ₹{price}. How much would you like to bid?"

        return jsonify({"reply": response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Something went wrong processing your request."}), 500

    

if __name__ == "__main__":
   app.run(debug=True, host="0.0.0.0", port=5000)
