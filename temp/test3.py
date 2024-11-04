from flask import Flask, request, redirect
import requests
import webbrowser

app = Flask(__name__)

# Replace these with your actual Client ID and Secret
CLIENT_ID = "gp762nuuoqcoxypju8c569th9wz7q5"
CLIENT_SECRET = "uonftl93psa5o3ckqhbz7zgda1y52l"

REDIRECT_URI = 'http://localhost:5000/callback'  # Must match the registered redirect URI

@app.route('/login')
def login():
    # Redirect the user to Twitch's authorization page
    auth_url = (
        f"https://id.twitch.tv/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=user:read:email"  # Specify required scopes here
    )
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Retrieve the authorization code from the callback
    code = request.args.get('code')

    # Exchange the code for an access token
    token_url = 'https://id.twitch.tv/oauth2/token'
    token_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(token_url, data=token_data)
    token_json = response.json()

    if 'access_token' in token_json:
        access_token = token_json['access_token']
        print("Access Token:", access_token)
        # Pass the token back to Tkinter or store it as needed
        return "Login successful! You can close this page."
    else:
        return "Error: Unable to retrieve access token."

if __name__ == '__main__':
    app.run(port=5000)
