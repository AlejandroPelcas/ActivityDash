import requests

def refresh_access_token(auth_url, client_id, client_secret,refresh_token):
    # Need new access token to use app every once in while
    # returns new refreshed token
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': "refresh_token",
        'f': 'json'
    }

    response = requests.post(auth_url, data=payload, verify=False)
    access_token = response.json()['access_token']
    print("Requesting Token...\n")
    return access_token