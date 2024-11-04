
# from openai import OpenAI
#
# api_key = "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"
# client = OpenAI(api_key=api_key)
# completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": "Write a haiku about recursion in programming."
#         }
#     ]
# )
#
# print(completion.choices[0].message)

import speech_recognition as sr
import socket
import time
import threading
import requests
from flask import Flask, request, redirect
import webbrowser

# Twitch app credentials
CLIENT_ID = "blsc7q9tyyit2ey3hcd6gzhn4w24ms"
CLIENT_SECRET = "n6u4wmd23g5uc58stvia43pqo5okk7"


from flask import Flask, redirect, request, url_for, session
import requests

app = Flask(__name__)
  # Replace with a secure secret key for session management

# Twitch Client Information
# Replace with your Twitch Client Secret
REDIRECT_URI = 'http://localhost/auth/callback'  # Redirect URI configured in Twitch Console

# OAuth URLs and scopes
AUTHORIZATION_BASE_URL = "https://id.twitch.tv/oauth2/authorize"
TOKEN_URL = "https://id.twitch.tv/oauth2/token"
SCOPES = 'user:read:email'  # Adjust scopes based on your app's requirements

@app.route('/')
def home():
    """Homepage with login link."""
    return '<a href="/login">Log in with Twitch</a>'

@app.route('/login')
def login():
    """Step 1: Redirect user to Twitch for authorization."""
    auth_url = (
        f"{AUTHORIZATION_BASE_URL}?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={SCOPES}"
    )
    print(auth_url)
    return redirect(auth_url)

@app.route('/auth/callback')
def auth_callback():
    """Step 2: Handle Twitch's authorization response and exchange the code for an access token."""
    code = request.args.get('code')
    if not code:
        return "Error: No code provided by Twitch", 400

    # Exchange code for token
    token_payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }
    token_response = requests.post(TOKEN_URL, data=token_payload)

    # Check if token exchange was successful
    if token_response.status_code == 200:
        token_data = token_response.json()
        access_token = token_data['access_token']
        session['access_token'] = access_token  # Store token in session
        return f"Logged in successfully! Access Token: {access_token[:10]}..."
    else:
        return f"Error: Failed to retrieve access token. {token_response.json()}", 400

@app.route('/logout')
def logout():
    """Log out by clearing the session."""
    session.pop('access_token', None)
    return "Logged out successfully."

@app.route('/profile')
def profile():
    """Retrieve the user's Twitch profile information using the access token."""
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))

    # Use the access token to access the Twitch API
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': CLIENT_ID
    }
    profile_response = requests.get('https://api.twitch.tv/helix/users', headers=headers)

    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        return f"User Profile: {profile_data['data'][0]}"
    else:
        return "Error: Failed to retrieve profile information."

if __name__ == '__main__':
    app.run(debug=True)


