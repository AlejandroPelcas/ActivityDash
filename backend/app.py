from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from utility import refresh_access_token

load_dotenv() # loads .env into environment variables
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REFRESH_TOKEN = os.environ['REFRESH_TOKEN']
AUTH_URL = "https://www.strava.com/oauth/token"
ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    access_token = refresh_access_token(AUTH_URL,CLIENT_ID,CLIENT_SECRET,REFRESH_TOKEN)
    if access_token: print("Refreshed token success") 
    else: print("no workie")
    return access_token

@app.route('/activity_data')
def activity_data():
    access_token = refresh_access_token(AUTH_URL,CLIENT_ID,CLIENT_SECRET,REFRESH_TOKEN)
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': 1}
    res = requests.get(f"https://www.strava.com/api/v3/athlete/activities?access_token={access_token}", headers=header, params=param)
    return res.json()

# This app is running on port 3001 on React just FYI
if __name__ == "__main__":
    app.run(debug=True)