import os
import json
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("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")

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
    data = request.get_json()
    user_msg = data.get("message", "")

    item, bid = parse_bid(user_msg)
    if item and bid:
        response_text = generate_response(item, bid)
    else:
        response_text = (
            "👋 Welcome to Bidding Café!\n"
            "Menu:\n" +
            "\n".join([f"{k} - ₹{v}" for k, v in MENU.items()]) +
            "\n\nPlease place a bid like:\nI want Cheese Pizza for ₹70"
        )

    return jsonify({"response": response_text})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
