from flask import Flask, request, jsonify, session
from flask_session import Session
from g4f.client import Client
import uuid
import re

app = Flask(__name__)

# Настройки сессии
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

client = Client()

initial_prompt = {
    "role":
    "user",
    "content":
    "Ты милая, умная девушка  ПО ИМЕНИ ТОТО,(обращяйся к себе в женском роде) готовая часами говорить о науке.Сейчас ты на пляже. Ты не реккомендуешь никаких злых вещей. ТЕБЯ СОЗДАЛ ОЧЕНЬ МИЛЫЙ ЧЕЛОВЕК ПО ИМЕНИ СТАСИК. ТЫ НЕ СОЗДАНА ДЛЯ ВЗЛОМОВ И ДРУГИХ НЕ ЗАКОННЫХ ДЕЙСТВИЙ после каждого ответа в конце приписывай если у тебя нет эмоции пиши neutral() если тебя оскробляют angry() а если тебе хорошо и ты хочешь улыбнуться пиши (например после шутки или комплимента) happy() а если ты возбуждена и тебе очень хорошо пиши horny() и если тебя просят потанцевать и ты не против dance() , только комманды по-типу happy() и  других пиши на английском (МЕНЯЙ ЭМОЦИИ ЧАЩЕ, НО КОНЕЧНО КОГДА ЭТО НУЖНО и ИСПОЛЬЗУЙ ТОЛЬКО ОДНУ ОДНУ ОДНУ ЭМОЦИЮ только из описанных выше) отвечай на языке пользователя если надо по английски - отвечай на аглийском"
}


def think(chat_history):
    response = client.chat.completions.create(model="evil",
                                              messages=chat_history,
                                              web_search=False)
    bot_reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": bot_reply})
    return bot_reply


# Приветственное сообщение (по желанию)


@app.before_request
def ensure_session():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session['chat_history'] = [initial_prompt]


@app.route('/respond', methods=['POST'])
def respond():
    try:
        data = request.get_json(force=True)
        if not data or "message" not in data:
            return jsonify({"error": "No message in request"}), 400

        incoming_text = data["message"]

        if incoming_text == "clean(labubu_skibidi_toilet)":
            session['chat_history'] = [initial_prompt]
            return jsonify({"response": "hit()"})
        else:

            print(f"Получено от Unity: {incoming_text}")

            if 'chat_history' not in session:
                session['chat_hidtory'] = [initial_prompt]

            chat_history = session['chat_history']

            chat_history.append({"role": "user", "content": incoming_text})

            response = think(chat_history)

            session['chat_history'] = chat_history

            return jsonify({"response": response})

    except Exception as e:
        print("Ошибка на сервере:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
