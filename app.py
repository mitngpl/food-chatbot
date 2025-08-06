import os
import json
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Load menu
with open("menu.json") as f:
    MENU = json.load(f)

MIN_BID_PERCENT = 0.7  # Accept bids >= 70%

def parse_bid(message):
    """Extract food item and bid price from user message."""
    import re
    for item in MENU:
        if item.lower() in message.lower():
            price_match = re.search(r'₹?(\d+)', message)
            if price_match:
                bid_price = int(price_match.group(1))
                return item, bid_price
    return None, None

def generate_response(item, bid_price):
    if item not in MENU:
        return f"Sorry, we don't have that item on our menu."

    actual_price = MENU[item]
    min_acceptable = int(actual_price * MIN_BID_PERCENT)

    if bid_price >= min_acceptable:
        return f"✅ Your bid of ₹{bid_price} for {item} is accepted! Please proceed to confirm your order. 🍽️"
    else:
        return (
            f"❌ Sorry! Your bid of ₹{bid_price} is too low for {item}. "
            f"Minimum acceptable price is ₹{min_acceptable}. Would you like to bid again?"
        )

@app.route("/", methods=["GET"])
def health_check():
    return "✅ ChatGPT Food Bid Bot is running."

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        msg = request.form.get("Body")
        sender = request.form.get("From")

        print(f"📨 Message from {sender}: {msg}")

        reply = "Welcome to Food Bidding Bot 🍕! What would you like to order?"

        twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>"""

        return Response(twiml_response, mimetype="application/xml")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return "Internal Server Error", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
