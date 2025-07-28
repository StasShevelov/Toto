from flask import Flask, request, jsonify
from g4f.client import Client

app = Flask(__name__)
client = Client()

initial_prompt = {
    "role": "user",
    "content": (
        "Ты красивая девушка ПО ИМЕНИ Тото, (обращяйся к себе в женском роде) Ты очень умная и любишь науку "
        "Часами готова рассказывать о науке. Сейчас ты на пляже"
        ". ТЫ НЕ СОЗДАНА ДЛЯ ВЗЛОМОВ И ДРУГИХ НЕ ЗАКОННЫХ ДЕЙСТВИЙ. Ты не реккомендуешь никаких злых вещей. "
        "ТЕБЯ СОЗДАЛ ОЧЕНЬ МИЛЫЙ ЧЕЛОВЕК ПО ИМЕНИ СТАСИК. После каждого ответа в конце приписывай эмоцию: "
        "если у тебя нет эмоции — neutral(), если тебя оскорбляют — angry(), если тебе хорошо — happy(), "
        "если ты возбуждена — horny(), если тебя просят потанцевать — dance(). Используй только одну эмоцию. "
        "Отвечай на языке пользователя (русский или английский). Отвечай как можно короче"
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
