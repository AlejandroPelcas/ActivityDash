from flask import Flask, jsonify, Response
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from utility import refresh_access_token,activity_plot, get_time_and_distances
import matplotlib.pyplot as plt
from db import init_db, get_db

# create the sqlite table in not exist yet
init_db()

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

@app.route('/check-token', methods=['GET'])
def check_token():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT access_token, refresh_token, expires_at
        FROM token
        ORDER BY id DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({
            "has_token": False
        })

    return jsonify({
        "has_token": True,
        "access_token": row[0],
        "refresh_token": row[1],
        "expires_at": row[2]
    })

@app.route('/refresh-token', methods=["POST"])
def refresh_token():
    print("refresh_access_token activated")
    token_data = refresh_access_token(AUTH_URL, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
    if token_data:
        print(f"Refreshed token success: Data = {token_data}")
        
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM token") # keep only 1 token
        cursor.execute("""
            INSERT INTO token (access_token, refresh_token, expires_at)
            VALUES (?,?,?)
            """, (
                token_data['access_token'],
                token_data['refresh_token'],
                token_data['expires_at']
        ))

        conn.commit()
        conn.close()

        return jsonify(token_data)
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
