from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Chatbot API is running!'

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.json
    user_message = data.get('message', '')

    response = requests.post(
        'https://api.groq.com/openai/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {os.environ.get("GROQ_API_KEY")}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'llama3-8b-8192',
            'messages': [
                {'role': 'system', 'content': 'You are a friendly chatbot. Keep replies short and conversational.'},
                {'role': 'user', 'content': user_message}
            ],
            'max_tokens': 200
        }
    )

    result = response.json()
    bot_reply = result['choices'][0]['message']['content']
    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
