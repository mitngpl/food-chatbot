import os
import json
import openai
import traceback
from flask import Flask, request, jsonify
from dotenv import load_dotenv

app = Flask(__name__)

# Load menu from JSON file
try:
    with open("menu.json", "r") as f:
        menu = json.load(f)
except Exception as e:
    print("❌ Could not load menu.json:", e)
    menu = {}

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_bidding(message):
    try:
        menu_items = "\n".join([f"{item.title()}: ₹{price}" for item, price in menu.items()])

        prompt = f"""
You are a witty and polite food ordering bot at a cafe.
Here is the menu:
{menu_items}

A customer sends this message: "{message}"

Your job is to respond in a friendly, funny tone:
- If the item exists and their offer is in 20-30% range of actual price, accept happily but try to negotiate once or twice.
- If offer is low, reject with a light joke.
- If item is not found, suggest valid items.

Respond in 1–3 short sentences. Use emojis where appropriate.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You're a funny and helpful café assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.8
        )

        reply = response['choices'][0]['message']['content'].strip()
        return reply

    except Exception as e:
        print("❌ GPT Error:", e)
        return "🤖 Sorry, something went wrong while generating your response."


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
