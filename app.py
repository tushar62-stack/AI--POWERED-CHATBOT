from flask import Flask, render_template, request, jsonify
from models.chatbot_model import Chatbot
from database import init_db, save_chat

app = Flask(__name__)
chatbot = None  
init_db()

def get_chatbot():
    """Lazy initialization of chatbot - only loads when first needed"""
    global chatbot
    if chatbot is None:
        chatbot = Chatbot()
    return chatbot

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_msg = data.get("message", "")

        if not user_msg:
            return jsonify({"reply": "Please type something!"})

        print(f"Received message: {user_msg}")
        
        
        print("Getting chatbot instance...")
        bot = get_chatbot()
        print("Chatbot instance ready, getting response...")
        
        bot_reply = bot.get_response(user_msg)
        print(f"Got reply: {bot_reply}")
        
        save_chat(user_msg, bot_reply)

        return jsonify({"reply": bot_reply})
    except Exception as e:
        import traceback
        error_msg = f"Error: {str(e)}"
        print(f"Error in /ask route: {error_msg}")
        print(traceback.format_exc())
        return jsonify({"reply": error_msg}), 500

if __name__ == "__main__":
    print("Starting Flask server...")
    print("Server will be available at http://127.0.0.1:5000")
    print("Note: Chatbot model will load on first message (this may take a few minutes)")
    app.run(debug=True, host='127.0.0.1', port=5000)