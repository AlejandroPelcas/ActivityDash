import requests
import matplotlib.pyplot as plt
from io import BytesIO
import requests
from datetime import datetime
from flask import Flask, jsonify, Response
import os
from db import get_db
import time

def get_valid_token():
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
        # No token → force refresh
        return refresh_access_token()

    access_token, refresh_token, expires_at = row
    now = int(time.time())

    # Refresh 2 minutes early
    if expires_at - now < 120:
        return refresh_access_token()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_at": expires_at
    }

def get_time_and_distances(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    res = requests.get(
        "https://www.strava.com/api/v3/athlete/activities",
        headers=headers
    )

    activities = res.json()

    return [
        (a["start_date"], a["distance"])
        for a in activities
    ]

def refresh_access_token(auth_url, client_id, client_secret, refresh_token):
    res = requests.post(
        auth_url,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
    )

    data = res.json()

    if "access_token" not in data:
        raise Exception(f"Token refresh failed: {data}")

    # 🔥 IMPORTANT: overwrite refresh token
    os.environ["REFRESH_TOKEN"] = data["refresh_token"]

    return data

def activity_plot():
    data = get_time_and_distances()
    # Convert timestamps to datetime objects
    timestamps = [datetime.strptime(item[0], "%Y-%m-%dT%H:%M:%SZ") for item in data]
    distances = [item[1]/1000 for item in data]  # convert meters to km

    # Sort by date
    timestamps, distances = zip(*sorted(zip(timestamps, distances)))

    # Plot
    plt.figure(figsize=(12,6))
    plt.plot(timestamps, distances, marker='o', linestyle='-', color='blue')
    plt.title("Strava Activities: Distance over Time")
    plt.xlabel("Date")
    plt.ylabel("Distance (km)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    # plt.show()
    # Save plot to PNG in memory
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')
