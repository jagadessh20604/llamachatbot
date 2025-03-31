from flask import Flask, request, jsonify
from flask_cors import CORS
from together import Together
import os
from dotenv import load_dotenv
import traceback

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Together API
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    raise ValueError("TOGETHER_API_KEY environment variable is not set")

print(f"API Key loaded: {TOGETHER_API_KEY[:5]}...")  # Print first 5 chars of API key

Together.api_key = TOGETHER_API_KEY

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
        
        # Get the last message from the user
        last_message = messages[-1]["content"]
        print(f"Received message: {last_message}")  # Log the received message
        
        # Generate response using Together API with Llama model
        print("Sending request to Together API...")  # Log before API call
        response = Together().inference(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            prompt=last_message,
            max_tokens=1024,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1.1,
        )
        print("Received response from Together API")  # Log after API call
        print(f"Response content: {response['output']['choices'][0]['text']}")  # Log the response
        
        return jsonify({"response": response['output']['choices'][0]['text']})
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")  # Log the error
        print("Full traceback:")  # Log the full traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Test the API directly
    print("Testing API...")
    test_response = Together().inference(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        prompt="Hello, how are you?",
        max_tokens=1024,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1.1,
    )
    print(f"Test response: {test_response['output']['choices'][0]['text']}")
    print("API test completed.")
    
    app.run(host='0.0.0.0', port=3001, debug=True) 