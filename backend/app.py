from flask import Flask, jsonify, Response
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from utility import refresh_access_token,activity_plot, get_time_and_distances
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime

load_dotenv()
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REFRESH_TOKEN = os.environ['REFRESH_TOKEN']
AUTH_URL = "https://www.strava.com/oauth/token"
ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"

app = Flask(__name__)
CORS(app)

# This is where the address routes are stored
@app.route('/')
def index():
    access_token = refresh_access_token(AUTH_URL, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
    if access_token:
        print("Refreshed token success")
        return jsonify({"access_token": access_token})
    else:
        print("no workie")
        return jsonify({"error": "could not refresh"}), 400

@app.route('/refresh-token', methods=["POST"])
def refresh_token():
    print("refresh_access_token activated")
    access_token = refresh_access_token(AUTH_URL, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
    if access_token:
        print("Refreshed token success")
        return jsonify(access_token)
    else:
        print("no workie")
        return jsonify({"error": "could not refresh"}), 400

@app.route('/activity_data')
def activity_data():
    access_token = refresh_access_token(
        AUTH_URL, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN
    )

    print("Obtained Access TOKEN")

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "per_page": 200,
        "page": 1
    }

    res = requests.get(ACTIVITIES_URL, headers=headers, params=params)

    if not res.ok:
        print("RES NOT OK")
        return jsonify(res.json()), res.status_code

    return jsonify(res.json())


if __name__ == "__main__":
    app.run(debug=True)
