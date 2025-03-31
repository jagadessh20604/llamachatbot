from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging
from together import Together

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Get API key
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
if not TOGETHER_API_KEY:
    logger.error("TOGETHER_API_KEY not found in environment variables")
    raise ValueError("TOGETHER_API_KEY not found in environment variables")

# Set Together API key
Together.api_key = TOGETHER_API_KEY

@app.route('/api/health', methods=['GET'])
def health_check():
    logger.info("Health check endpoint called")
    response = make_response(jsonify({"status": "healthy"}))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/chat', methods=['POST'])
def chat():
    logger.info("Chat endpoint called")
    try:
        # Log request details
        logger.info(f"Request headers: {dict(request.headers)}")
        logger.info(f"Request data: {request.get_data()}")
        
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return make_response(jsonify({"error": "No data provided"}), 400)
        
        messages = data.get('messages', [])
        if not messages:
            logger.error("No messages in request")
            return make_response(jsonify({"error": "No messages provided"}), 400)
        
        # Get the last message
        last_message = messages[-1].get('content', '')
        logger.info(f"Received message: {last_message}")
        
        # Generate response using Together API
        response = Together().inference(
            prompt=last_message,
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            max_tokens=1024,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
        )
        
        # Log the response
        logger.info(f"API Response: {response}")
        
        # Extract the response text
        response_text = response['output']['choices'][0]['text']
        
        # Create response with CORS headers
        response = make_response(jsonify({
            "response": response_text
        }))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return make_response(jsonify({"error": str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True) 