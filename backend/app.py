from flask import Flask, request, jsonify
from flask_cors import CORS
from together import Together
import os

app = Flask(__name__)
CORS(app)

# Configure Together API
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    raise ValueError("TOGETHER_API_KEY environment variable is not set")

Together.api_key = TOGETHER_API_KEY

# Initialize Together client
client = Together()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        messages = data.get('messages', [])
        if not messages:
            return jsonify({"error": "No messages provided"}), 400
        
        # Generate response
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=messages
        )
        
        return jsonify({"response": response.choices[0].message.content})
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")  # Add logging
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True) 