from together import Together
import os

# Configure Together API
TOGETHER_API_KEY = "cd03108f4f3627d1d8ece9cb5fa5ba92f1ec082e9f0ba2abc8f09d80a14656e3"
Together.api_key = TOGETHER_API_KEY

def test_api():
    try:
        # Initialize Together client
        client = Together()
        print("Together client initialized successfully")

        # Test API call
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[{"role": "user", "content": "Say hello!"}]
        )
        
        print("Response received successfully:")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api() 