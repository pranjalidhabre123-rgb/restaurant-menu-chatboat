import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


MENU = """
Restaurant Menu:

PIZZAS:
1. Margherita Pizza - ₹199
2. Farmhouse Pizza - ₹299
3. Paneer Tikka Pizza - ₹329
4. Veggie Supreme Pizza - ₹349

STARTERS:
1. French Fries - ₹99
2. Veg Spring Rolls - ₹149
3. Paneer Tikka - ₹229

MAIN COURSE:
1. Paneer Butter Masala - ₹249
2. Veg Biryani - ₹199
3. Dal Tadka - ₹149

BEVERAGES:
1. Cold Coffee - ₹129
2. Fresh Lime Soda - ₹79
3. Masala Chai - ₹49
"""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    prompt = f"""
You are a helpful Restaurant Menu Chatbot.

Your job is to answer questions about the restaurant menu.

IMPORTANT INSTRUCTIONS:
- Answer using the menu information provided below.
- If the requested item is in the menu, mention its price.
- If the item is not in the menu, clearly say that it is not available.
- Do not invent menu items or prices.
- Keep answers short, friendly, and easy to understand.
- If the user asks for vegetarian items, suggest suitable vegetarian items from the menu.
- If the user asks for items under a budget, only suggest items within that budget.

RESTAURANT MENU:
{MENU}

CUSTOMER QUESTION:
{user_message}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        print("ERROR:", e)

        return jsonify({
            "reply": "Sorry, I am unable to respond right now."
        })


if __name__ == "__main__":
    app.run(debug=True)