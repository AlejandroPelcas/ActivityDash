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

    response = requests.post(auth_url, data=payload)  
    
    # If request failed, print the message
    if response.status_code != 200:
        print("Error refreshing token:", response.text)
        return None
    
    data = response.json()
    print("Requesting Token...\n")
    return data.get("access_token")