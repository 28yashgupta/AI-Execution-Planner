from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access variables
api_key = os.getenv("API_KEY")
from flask import Flask, request, jsonify
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="api_key")

# Define workflow templates
WORKFLOW_TEMPLATES = {
    "fetch api data": {
        "steps": ["Send request to API", "Parse response", "Save data to CSV"],
        "code": '''import requests
import csv

url = "https://api.example.com/data"
response = requests.get(url)
data = response.json()

with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(data.keys())
    writer.writerow(data.values())

print("Data saved to output.csv")'''
    },
    "analyze text sentiment": {
        "steps": ["Load text data", "Apply sentiment analysis model", "Return sentiment score"],
        "code": '''from textblob import TextBlob

text = "I love this product!"
sentiment = TextBlob(text).sentiment.polarity

print(f"Sentiment Score: {sentiment}")'''
    }
}

# Function to extract intent from query
def extract_intent(query):
    """Extracts intent using Google Gemini API."""
    prompt = f"Extract the intent of this query: '{query}'. Return only the intent as a single phrase."

    try:
        response = genai.generate_content("gemini-1.5-pro", prompt)
        if response and hasattr(response, "candidates"):
            intent = response.candidates[0].content.parts[0].text.strip().lower()
            print(f"Extracted Intent: {intent}")  # Debugging
            return intent
    except Exception as e:
        print(f"Gemini API Error: {e}")  # Debugging
        return "unknown"

    return "unknown"

# API route for generating workflows
@app.route("/generate_workflow", methods=["POST"])
def generate_workflow():
    """Handles user queries and maps them to execution steps."""
    data = request.json
    user_query = data.get("query")

    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    # Extract intent
    intent = extract_intent(user_query)

    # Match extracted intent with workflows
    for key, template in WORKFLOW_TEMPLATES.items():
        if key in intent:
            return jsonify({"intent": intent, "steps": template["steps"], "code": template["code"]})

    return jsonify({"message": "No matching workflow found. Please refine your query."})

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=8080)
