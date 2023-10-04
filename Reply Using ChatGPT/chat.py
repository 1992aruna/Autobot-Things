from flask import Flask, request, jsonify
import openai
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import gridfs
from pymongo import MongoClient

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
API_URL = os.getenv("API_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the Flask app
app = Flask(__name__)

# Set up your OpenAI API key
openai.api_key = OPENAI_API_KEY

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["chat_gpt"]
fs = gridfs.GridFS(db)

@app.route('/')
def home():
    return "WhatsApp Chatbot with GPT-3 is running!"

@app.route("/webhook", methods=['POST'])
def whatsapp_webhook():
    try:
        data = request.json
        # print("Webhook Payload:", data)  # Debug statement to print the entire payload

        number = data.get('waId', '')
        incoming_message = data.get('text', '').strip()  # Extract the incoming message

        # print("Incoming Message:", incoming_message)  # Debug statement

        # Generate a response using GPT-3.5 Turbo with the incoming message as the user's query
        answer = generate_answer(incoming_message)

        # print("Generated Answer:", answer)  # Debug statement

        # Send the response via WhatsApp
        send_message(number, answer)

        return jsonify({'status': 'Message sent'})

    except Exception as e:
        print(e)
        return 'Error processing message'

def generate_answer(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}  # Use the incoming WhatsApp message as the user's query
            ],
            temperature=0.7,
            max_tokens=150
        )

        answer = response.choices[0].message['content'].strip()
        return answer
    except Exception as e:
        return f"Error generating answer: {str(e)}"

def send_message(contact_number, message):
    headers = {
        'Authorization': ACCESS_TOKEN,
    }
    payload = {'messageText': message}

    try:
        url = f"{API_URL}/api/v1/sendSessionMessage/{contact_number}"
        response = requests.post(url=url, headers=headers, data=payload)
        return response.status_code
    except Exception as e:
        return f"Error sending message: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
