from flask import Flask, request, Response
import json
import traceback

app = Flask(__name__)

# Load menu from JSON file
try:
    with open("menu.json", "r") as f:
        menu = json.load(f)
except Exception as e:
    print("❌ Could not load menu.json:", e)
    menu = {}

def process_bidding(message):
    message = message.lower()

    for item in menu:
        if item in message:
            price_words = [int(s) for s in message.split() if s.isdigit()]
            if not price_words:
                return f"🤖 The regular price for {item.title()} is ₹{menu[item]}. Please quote your offer price."

            offer = price_words[0]
            if offer >= menu[item]:
                return f"✅ Deal! {item.title()} is accepted for ₹{offer}."
            else:
                return f"❌ Sorry, we cannot offer {item.title()} at ₹{offer}. Regular price is ₹{menu[item]}."
    
    return "🤖 Item not found in the menu. Please try ordering something from our menu: " + ", ".join(menu.keys())

@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Food Bidding Bot is live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        print("📥 Headers:", request.headers)
        print("📥 Body:", request.data.decode())

        if request.headers.get("Content-Type") == "application/x-www-form-urlencoded":
            incoming_msg = request.form.get("Body")
            sender = request.form.get("From")
        else:
            incoming_msg = "Unable to parse"
            sender = "Unknown"

        print(f"📨 From: {sender} | Message: {incoming_msg}")

        reply = process_bidding(incoming_msg)

        response_msg = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>"""

        return Response(response_msg, mimetype="application/xml")

    except Exception as e:
        print("❌ Exception occurred:", str(e))
        traceback.print_exc()
        return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
