from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# This holds the text response until your physical ESP32 robot downloads it
robot_speech_queue = "WAITING"
GROQ_API_KEY = "YOUR_NEW_FRESH_GROQ_KEY" # <-- PASTE YOUR REAL GROQ KEY HERE

@app.route("/")
def home():
    # This generates a super clean chat input dashboard right on your mobile browser
    return '''
    <html>
      <body style="font-family:sans-serif; text-align:center; padding:50px; background:#111; color:white;">
        <h2>🤖 Desk Robot Controller</h2>
        <input type="text" id="msg" placeholder="Type math problems or jokes..." style="width:80%; padding:15px; font-size:16px; margin-bottom:20px; border-radius:5px;"><br>
        <button onclick="send()" style="padding:15px 30px; font-size:16px; background:#00aa00; color:white; border:none; border-radius:5px; cursor:pointer;">Send to Robot</button>
        <p id="status" style="margin-top:20px; color:yellow; font-weight:bold;"></p>
        <script>
          async function send() {
            const txt = document.getElementById('msg').value;
            document.getElementById('status').innerText = "Groq AI is thinking...";
            await fetch('/chat?text=' + encodeURIComponent(txt));
            document.getElementById('status').innerText = "Sent! Robot is reading it now.";
            document.getElementById('msg').value = "";
          }
        </script>
      </body>
    </html>
    '''

@app.route("/chat")
def chat():
    global robot_speech_queue
    user_prompt = request.args.get('text', '')
    if not user_prompt:
        return "No text provided"

    try:
        # Send your phone's typed text directly to the ultra-fast Groq engine
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": user_prompt + " (Keep your answer short, under 12 words)"}]
        }
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=body, headers=headers)
        data = res.json()
        
        # Save the answer to the queue for the ESP32
        robot_speech_queue = data['choices'][0]['message']['content']
        return "Success"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/get_robot_speech")
def get_robot_speech():
    global robot_speech_queue
    msg = robot_speech_queue
    if robot_speech_queue != "WAITING":
        robot_speech_queue = "WAITING" # Clear queue immediately after the robot grabs it
    return msg

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
  
