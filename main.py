import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Fetch the key from Render's Environment Variables
GROQ_API_KEY = os.environ.get("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") 
robot_speech_queue = None

# This route keeps Render from killing the app
@app.route("/health")
def health():
    return "OK", 200

@app.route("/")
def home():
    return "Robot Bridge is Online."

@app.route("/chat")
def chat():
    global robot_speech_queue
    user_prompt = request.args.get('text', '')
    if not user_prompt: return "No text"
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    body = {
        "model": "llama3-8b-8192", 
        "messages": [{"role": "user", "content": user_prompt + " (Keep answer under 10 words)"}]
    }
    
    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=body, headers=headers)
        data = res.json()
        
        if 'error' in data:
            return f"API Error: {data['error'].get('message', 'Unknown Error')}"
            
        robot_speech_queue = data['choices'][0]['message']['content']
        return "Success"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/get_robot_speech")
def get_robot_speech():
    global robot_speech_queue
    if robot_speech_queue is None:
        return ""
    
    msg = robot_speech_queue
    robot_speech_queue = None 
    return msg

if __name__ == "__main__":
    # Ensure it listens on the port Render assigns
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
