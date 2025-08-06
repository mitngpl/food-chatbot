from flask import Flask, request, Response
import traceback
import re

app = Flask(__name__)

menu = {
    "cheese pizza": 100,
    "paneer momos": 80,
    "oreo shake": 90,
}

msg = incoming_msg.strip().lower()
response = ""

@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Food Bidding Bot is live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.get_json().get("message", "").strip().lower()
    response = ""

    # Match pattern: "I want to order <item> for <amount>"
    match = re.match(r"i want to order (.+?) for (\d+)", incoming_msg)
    if match:
        item = match.group(1).strip()
        bid_price = int(match.group(2))

        if item in menu:
            actual_price = menu[item]
            if bid_price >= actual_price * 0.8:
                response = f"✅ Bid Accepted for {item.title()} at ₹{bid_price}!"
            else:
                response = f"❌ Bid too low for {item.title()}! Minimum acceptable is ₹{int(actual_price * 0.8)}"
        else:
            response = "🚫 Sorry, that item is not on our menu."
    else:
        response = (
            "👋 Welcome to the Food Bidding Bot!\n"
            "🍽️ To place a bid, send: 'I want to order <item> for <amount>'.\n"
            "Example: 'I want to order cheese pizza for 70'"
        )

    return {"reply": response}, 200

    except Exception as e:
        print("❌ Exception occurred:", str(e))
        traceback.print_exc()
        return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
