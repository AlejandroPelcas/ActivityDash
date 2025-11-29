from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from utility import refresh_access_token

load_dotenv()
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REFRESH_TOKEN = os.environ['REFRESH_TOKEN']
AUTH_URL = "https://www.strava.com/oauth/token"
ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    access_token = refresh_access_token(AUTH_URL, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
    if access_token:
        print("Refreshed token success")
        return jsonify({"access_token": access_token})
    else:
        print("no workie")
        return jsonify({"error": "could not refresh"}), 400


@app.route('/activity_data')
def activity_data():
    access_token = refresh_access_token(AUTH_URL, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    params = {
        "per_page": 200,
        "page": 1
    }

    # TODO: Need to automate getting new refresh token for this to work
    # res = requests.get(ACTIVITIES_URL, headers=headers, params=params)
    res = requests.get("https://www.strava.com/api/v3/athlete/activities?access_token=d38b0fae014de92cf92d72dbc944af8c85141e2c")
    return jsonify(res.json())


if __name__ == "__main__":
    app.run(debug=True)
