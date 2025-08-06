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
    try:
        # Debug log entire request
        print("📥 Headers:", request.headers)
        print("📥 Body:", request.data.decode())
        
        # Check content type
        if request.headers.get("Content-Type") == "application/x-www-form-urlencoded":
            # Twilio sends WhatsApp messages in form format
            incoming_msg = request.form.get("Body")
            sender = request.form.get("From")
        else:
            incoming_msg = "Unable to parse"
            sender = "Unknown"

        print(f"📨 From: {sender} | Message: {incoming_msg}")

        # Sample response
        reply = "👋 Welcome to the Food Bidding Bot! What would you like to order?"

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
