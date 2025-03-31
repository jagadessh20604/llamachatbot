import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Generative AI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# List all available models
for m in genai.list_models():
    print(f"Model name: {m.name}")
    print(f"Display name: {m.display_name}")
    print(f"Description: {m.description}")
    print(f"Generation methods: {m.supported_generation_methods}")
    print("-" * 50) 