from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return 'Chatbot API is running!'

@app.route('/chat', methods=['GET', 'POST', 'OPTIONS'])
def chat():
    if request.method == 'GET':
        return jsonify({'reply': 'API is working! Please use POST method.'})
    
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        return response, 200

    data = request.json
    user_message = data.get('message', '')

    groq_response = requests.post(
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

    result = groq_response.json()
    bot_reply = result['choices'][0]['message']['content']
    
    response = jsonify({'reply': bot_reply})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
