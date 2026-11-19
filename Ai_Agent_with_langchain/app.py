from flask import Flask, render_template, request, jsonify
from main import agent

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/send", methods=["POST"])
def send():
    print("FORM:", request.form)                     # debug
    print("JSON:", request.get_json(silent=True))    # debug

    data = request.get_json(silent=True) or request.form
    user_message = data.get("user_input")

    if not user_message:
        return jsonify({"error": "No message received"}), 400

    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_message}]},
        {"configurable": {"thread_id": "1"}},
    )

    reply = response["messages"][-1].text
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)