from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Application start"

@app.route('/api/message')
def message():
    return jsonify({"message" : "testing message api"})

if __name__ == "__main__":
    app.run(debug=True)