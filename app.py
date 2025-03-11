from flask import Flask, render_template, request, jsonify 
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import os

app = Flask(__name__)



# Load API Key 
openai_api_key = "Your_API_Key"

# Initialize GPT-4o Mini Model with Optimized Settings
llm = ChatOpenAI(
    model_name="gpt-4o-mini", 
    openai_api_key=openai_api_key, 
    temperature=0.2,  # More factual responses
    max_tokens=300,  # Limit response length
    streaming=True  # Enable real-time response streaming
)

# Store chat history for sessions
message_histories = {}

# Function to retrieve the session-specific message history
def get_session_history(session_id: str):
    if session_id not in message_histories:
        message_histories[session_id] = ChatMessageHistory()
    
    # Keep the last 10 exchanges instead of 5
    history = message_histories[session_id]
    if len(history.messages) > 10:
        history.messages = history.messages[-10:]
    
    return history

# Create a conversation chain with memory
conversation = RunnableWithMessageHistory(
    llm,
    get_session_history=get_session_history
)

@app.route('/')
def home():
    return render_template('index.html')  # Loads the chatbot UI

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    session_id = request.remote_addr  # Use IP as session ID

    if not user_message.strip():
        return jsonify({"error": "Message cannot be empty."})

    try:
        # Use conversation memory to process the query with system message
        bot_reply = conversation.invoke(
            {"input": user_message},
            config={"configurable": {"session_id": session_id}}
        )

        return jsonify({"message": bot_reply.content})  # Extract response text

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500  # Handle API errors

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Run on port 5001 to avoid conflicts
