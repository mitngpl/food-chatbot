from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Food Bidding Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("📥 Incoming JSON:", data)

        if not data or "message" not in data:
            return jsonify({"reply": "❌ Invalid request. No message received."}), 400

        message = data["message"].lower()
        print("📩 Message:", message)

        # Simple bidding logic
        if "cheese pizza" in message:
            if "70" in message or "60" in message:
                return jsonify({"reply": "❌ Sorry, we can't offer Cheese Pizza at that price."})
            elif "100" in message:
                return jsonify({"reply": "✅ Deal! Cheese Pizza for ₹100 is accepted."})
            else:
                return jsonify({"reply": "🤖 Please quote a price for Cheese Pizza."})
        else:
            return jsonify({"reply": "🤖 We don't have that item. Please check the menu."})

    except Exception as e:
        print("❌ Error occurred:", str(e))
        return jsonify({"reply": "❌ Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
