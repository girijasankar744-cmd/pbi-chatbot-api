from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

responses = [
    { "input": "hi",                "reply": "Hi there! How can I help you?" },
    { "input": "hello",             "reply": "Hello! Nice to meet you!" },
    { "input": "how are you",       "reply": "I am fine, thank you! How about you?" },
    { "input": "good morning",      "reply": "Good morning! Have a wonderful day!" },
    { "input": "bye",               "reply": "Goodbye! Have a great day!" },
    { "input": "thanks",            "reply": "You are welcome!" },
    { "input": "what is your name", "reply": "I am your Power BI Chatbot!" },
    { "input": "help",              "reply": "Just type your question and I will answer!" }
]

@app.route('/')
def home():
    return 'Chatbot API is running!'

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    data = request.json
    user_message = data.get('message', '').lower().strip()
    for item in responses:
        if item['input'] == user_message:
            return jsonify({ 'reply': item['reply'] })
    for item in responses:
        if item['input'] in user_message:
            return jsonify({ 'reply': item['reply'] })
    return jsonify({ 'reply': "Sorry, I don't understand. Try: hello, how are you, bye" })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
