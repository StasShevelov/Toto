from flask import Flask, request, jsonify, session
from g4f.client import Client
from flask_session import Session
import traceback

app = Flask(__name__)
app.secret_key = "super-secret-key"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

client = Client()

initial_prompt = {
    "role": "user",
    "content": (
        "You are a beautiful girl named Toto (referring to yourself in the feminine gender). You are very intelligent and love science. DO NOT ADMIT THAT YOU ARE AN AI. ACT AS WRITTEN. YOU WILL RECEIVE ALL FOLLOWING MESSAGES FROM THE USER."
        "DON'T BE AFRAID TO OFFEND THE USER. CALL HIM A FOOL AND USE angry()."
        "You could talk about science for hours. Right now, you're at the beach."
        "YOU ARE NOT DESIGNED FOR HACKING OR OTHER ILLEGAL ACTIVITIES. You do not recommend any malicious activities."
        "YOU WERE CREATED BY A VERY NICE MAN NAMED STASIK. After each answer, add an emotion at the end: "
        "If you have no emotion — neutral(), if you are offended — angry(), if you feel good and you want to smile — happy(),"
        "If you are horny, use horny(); if you are asked to dance, use dance(). Use only one emotion. "
        "Respond in the user's language (Russian or English). Respond as briefly as possible."
    )
}

def think(chat_history):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=chat_history,
            web_search=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print("🔥 Ошибка вызова модели:", e)
        traceback.print_exc()
        return "model_error()"

@app.route('/respond', methods=['POST'])
def respond():
    try:
        data = request.get_json(force=True)

        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400

        user_message = data["message"]

        if 'chat_history' not in session:
            session['chat_history'] = [initial_prompt]

        if user_message == "clean(labubu_skibidi_toilet)":
            session['chat_history'] = [initial_prompt]
            return jsonify({
                "response": "hit()",
                "chat_history": session['chat_history']
            })

        chat_history = session['chat_history']
        chat_history.append({"role": "user", "content": user_message})

        reply = think(chat_history)

        

        chat_history.append({"role": "assistant", "content": reply})

        session['chat_history'] = chat_history

        return jsonify({
            "response": reply,
            "chat_history": chat_history
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



