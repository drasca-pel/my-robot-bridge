import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Ensure your key is in Render Environment Variables
GROQ_API_KEY = os.environ.get("GROQ_API_KEY") 
robot_speech_queue = None

@app.route("/chat")
def chat():
    global robot_speech_queue
    user_prompt = request.args.get('text', '')
    if not user_prompt: return "No text"
    
    headers = {"Authorization": f"Bearer {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}", "Content-Type": "application/json"}
    body = {
        "model": "llama3-8b-8192", 
        "messages": [{"role": "user", "content": user_prompt + " (Keep answer under 10 words)"}]
    }
    
    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=body, headers=headers)
        data = res.json()
        
        # Check if Groq sent an error message instead of 'choices'
        if 'error' in data:
            return f"API Error: {data['error']['message']}"
            
        robot_speech_queue = data['choices'][0]['message']['content']
        return "Success"
    except Exception as e:
        return f"Error: {str(e)}"

# ... (rest of your get_robot_speech code remains the same)
