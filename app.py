import streamlit as st
from together import Together

# Configure Together API
TOGETHER_API_KEY = "cd03108f4f3627d1d8ece9cb5fa5ba92f1ec082e9f0ba2abc8f09d80a14656e3"
Together.api_key = TOGETHER_API_KEY

# Set page config
st.set_page_config(
    page_title="Llama Chatbot",
    page_icon="🦙",
    layout="centered"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Together client
@st.cache_resource
def get_together_client():
    return Together()

# Display chat title
st.title("🦙 Llama Chatbot")
st.write("Welcome! Let's chat with Llama 3.3 70B!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get response from model
    try:
        # Get Together client
        client = get_together_client()
        
        # Prepare messages for the API
        messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
        
        # Generate response
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=messages
        )
        
        # Get the response content
        response_content = response.choices[0].message.content
        
        # Display bot response
        with st.chat_message("assistant"):
            st.markdown(response_content)
        
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add a sidebar with information
with st.sidebar:
    st.title("About")
    st.write("This chatbot is powered by Llama 3.3 70B Instruct Turbo Free model.")
    st.write("Try asking questions or having a conversation!")