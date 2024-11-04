import os
from flask import Flask, redirect, request, url_for, session
import requests

class TwitchOAuth:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authorization_base_url = "https://id.twitch.tv/oauth2/authorize"
        self.token_url = "https://id.twitch.tv/oauth2/token"
        self.scopes = 'user:read:email'
        self.access_token = None

    def get_auth_url(self):
        """Builds the authorization URL to redirect the user to Twitch for login."""
        auth_url = (
            f"{self.authorization_base_url}?client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&response_type=code"
            f"&scope={self.scopes}"
        )
        return auth_url

    def exchange_code_for_token(self, code):
        """Exchanges the authorization code for an access token."""
        token_payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }
        token_response = requests.post(self.token_url, data=token_payload)

        if token_response.status_code == 200:
            token_data = token_response.json()
            self.access_token = token_data['access_token']
            return self.access_token
        else:
            raise Exception(f"Failed to retrieve access token: {token_response.json()}")

    def get_access_token(self):
        """Returns the stored access token."""
        return self.access_token

    def get_user_profile(self):
        """Retrieves the user's Twitch profile information using the access token."""
        if not self.access_token:
            raise Exception("Access token is not available.")

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Client-Id': self.client_id
        }
        profile_response = requests.get('https://api.twitch.tv/helix/users', headers=headers)

        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            return profile_data['data'][0]
        else:
            raise Exception("Failed to retrieve profile information.")

# Flask app setup
app = Flask(__name__)
 # Replace with a secure secret key for session management

# Initialize Twitch OAuth
CLIENT_ID = "blsc7q9tyyit2ey3hcd6gzhn4w24ms"
CLIENT_SECRET = "n6u4wmd23g5uc58stvia43pqo5okk7"
REDIRECT_URI = 'http://localhost:5000/auth/callback'
twitch_oauth = TwitchOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

@app.route('/')
def home():
    """Homepage with login link."""
    return '<a href="/login">Log in with Twitch</a>'

@app.route('/login')
def login():
    """Redirect user to Twitch for authorization."""
    auth_url = twitch_oauth.get_auth_url()
    return redirect(auth_url)

@app.route('/auth/callback')
def auth_callback():
    """Handle Twitch's authorization response and exchange the code for an access token."""
    code = request.args.get('code')
    if not code:
        return "Error: No code provided by Twitch", 400

    try:
        access_token = twitch_oauth.exchange_code_for_token(code)
        session['access_token'] = access_token  # Store token in session if needed
        os._exit(0)  # Shut down the server after obtaining the token
    except Exception as e:
        return str(e), 400

@app.route('/logout')
def logout():
    """Log out by clearing the session."""
    session.pop('access_token', None)
    return "Logged out successfully."

@app.route('/profile')
def profile():
    """Retrieve the user's Twitch profile information."""
    try:
        profile_data = twitch_oauth.get_user_profile()
        return f"User Profile: {profile_data}"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
