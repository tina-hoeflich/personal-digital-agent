from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# das sagt, dass die api routes aus api/input.py benutzt werden sollen
import api.user.input

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
