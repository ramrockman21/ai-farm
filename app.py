from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

from utils.dataset_search import search_dataset

# ----------------------------
# App Setup
# ----------------------------
app = Flask(__name__)
CORS(app)

# ----------------------------
# Gemini API Setup
# ----------------------------
client = genai.Client(api_key="AIzaSyAKHyA7XHAcClEHievYcTP2qM_EhLaaB5A")  


# ----------------------------
# Home Route
# ----------------------------
@app.route('/')
def home():
    return "🌾 AI Farmer Assistant Backend Running!"


# ----------------------------
# Ask Route (Main API)
# ----------------------------
@app.route('/ask', methods=['POST'])
def ask():
    data = request.json

    # Inputs
    question = data.get('question', '')
    crop = data.get('crop', '')
    location = data.get('location', 'India')

    # ----------------------------
    # Step 1: Search Dataset
    # ----------------------------
    dataset_answer = search_dataset(crop, question)

    if dataset_answer:
        return jsonify({
            "source": "dataset",
            "answer": dataset_answer
        })

    # ----------------------------
    # Step 2: AI (Gemini)
    # ----------------------------
    prompt = f"""
    You are an expert agricultural advisor helping farmers.

    Farmer Location: {location}
    Crop: {crop}

    Question: {question}

    Instructions:
    - Give practical, step-by-step advice
    - Keep it simple
    - Answer in Malayalam
    """

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        answer = response.text

    except Exception as e:
        answer = f"Error: {str(e)}"

    return jsonify({
        "source": "ai",
        "answer": answer
    })


# ----------------------------
# Run App
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)