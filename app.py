from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Chatbot API is running!'

@app.route('/chat', methods=['POST'])
def chat():

    try:

        data = request.get_json()

        user_message = data.get('message', '')

        api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            return jsonify({
                'reply': 'GROQ API key missing'
            }), 500

        groq_response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'llama3-8b-8192',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a friendly chatbot.'
                    },
                    {
                        'role': 'user',
                        'content': user_message
                    }
                ],
                'max_tokens': 200
            }
        )

        print(groq_response.status_code)
        print(groq_response.text)

        result = groq_response.json()

        if 'choices' not in result:
            return jsonify({
                'reply': result
            }), 500

        bot_reply = result['choices'][0]['message']['content']

        return jsonify({
            'reply': bot_reply
        })

    except Exception as e:

        print(str(e))

        return jsonify({
            'reply': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
