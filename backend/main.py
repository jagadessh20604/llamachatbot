from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from together import Together
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Together API
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "cd03108f4f3627d1d8ece9cb5fa5ba92f1ec082e9f0ba2abc8f09d80a14656e3")
Together.api_key = TOGETHER_API_KEY

try:
    # Initialize Together client
    client = Together()
    logger.info("Together client initialized successfully")
except Exception as e:
    logger.error(f"Error initializing Together client: {e}")
    raise

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    response: str

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        logger.info("Received chat request")
        
        # Convert messages to the format expected by Together API
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Generate response
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=messages
        )
        
        logger.info("Successfully generated response")
        return ChatResponse(response=response.choices[0].message.content)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 