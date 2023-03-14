from flask import Flask, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    message = "Hallo ich bin J.A.R.V.I.S."
    print(message)
    return message

@app.route('/input', methods=['POST'])
def text_input():
    message = request.get_data(as_text=True)
    responses = ["Hello, i'm J.A.R.V.I.S.",
                 "How are you?",
                 "What's up?",
                 "Nice to meet you!"]
    response = random.choice(responses)
    app.logger.info("Nachricht empfangen: {}; responding with: {}".format(message, response))
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
