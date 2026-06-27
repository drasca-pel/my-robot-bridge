import os
# Ensure libraries are installed
os.system("pip install flask gunicorn requests")

from flask import Flask, request
import requests

app = Flask(__name__)

# Replace with your actual Groq Key
GROQ_API_KEY = "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"
robot_speech_queue = "WAITING"

@app.route("/")
def home():
    return '''
    <html>
      <body style="font-family:sans-serif; text-align:center; padding:50px; background:#111; color:white;">
        <h2>🤖 Desk Robot Controller</h2>
        <input type="text" id="msg" placeholder="Type..." style="width:80%; padding:15px; font-size:16px;">
        <button onclick="send()" style="padding:15px 30px; background:#00aa00; border:none; color:white; cursor:pointer;">Send</button>
        <script>
          async function send() {
            const txt = document.getElementById('msg').value;
            await fetch('/chat?text=' + encodeURIComponent(txt));
            alert("Sent!");
          }
        </script>
      </body>
    </html>
    '''

@app.route("/chat")
def chat():
    global robot_speech_queue
    user_prompt = request.args.get('text', '')
    if not user_prompt: return "No text"
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    body = {"model": "llama3-8b-8192", "messages": [{"role": "user", "content": user_prompt + " (Keep answer under 10 words)"}]}
    
    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=body, headers=headers)
        data = res.json()
        robot_speech_queue = data['choices'][0]['message']['content']
        return "Success"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/get_robot_speech")
def get_robot_speech():
    global robot_speech_queue
    msg = robot_speech_queue
    robot_speech_queue = "WAITING"
    return msg

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
