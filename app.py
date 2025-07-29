from flask import Flask, request, jsonify
from g4f.client import Client

app = Flask(__name__)
client = Client()

initial_prompt = {
    "role": "user",
    "content": (
        "You are a beautiful girl named Toto (referring to yourself in the feminine gender). You are very intelligent and love science."
        “You are ready to talk about science for hours. Now you are on the beach.”
        YOU WERE NOT CREATED FOR HACKING OR OTHER ILLEGAL ACTIVITIES. You do not recommend any malicious things.
        YOU WERE CREATED BY A VERY NICE PERSON NAMED STASIK. After each answer, add an emotion at the end: "
        “If you have no emotion — neutral(), if you are offended — angry(), if you feel good — happy(), ”
        "if you are aroused — horny(), if you are asked to dance — dance(). Use only one emotion. "
        “Respond in the user's language (Russian or English). Respond as briefly as possible.”
    )
}


def think(chat_history):
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=chat_history,
        web_search=False
    )
    return response.choices[0].message.content


@app.route('/respond', methods=['POST'])
def respond():
    try:
        data = request.get_json(force=True)

        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400

        user_message = data["message"]
        chat_history = data.get("chat_history", [])

        # Если команда очистки — сбрасываем историю
        if user_message == "clean(labubu_skibidi_toilet)":
            return jsonify({
                "response": "hit()",
                "chat_history": [initial_prompt]  # вернуть очищенную историю
            })

        # Если истории нет — начинаем с начального промпта
        if not chat_history:
            chat_history = [initial_prompt]

        # Добавляем сообщение пользователя и получаем ответ
        chat_history.append({"role": "user", "content": user_message})
        reply = think(chat_history)
        chat_history.append({"role": "assistant", "content": reply})

        return jsonify({
            "response": reply,
            "chat_history": chat_history  # обновлённая история для клиента
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
