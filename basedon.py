# https://stackoverflow.com/questions/57580411/storing-spotify-token-in-flask-session-using-spotipy

from flask import Flask, render_template, redirect, request, session, make_response, session, redirect
import spotipy
import spotipy.util as util
from credentz import *
import requests
app = Flask(__name__)

app.secret_key = SSK

API_BASE = 'https://accounts.spotify.com'

# Make sure you add this to Redirect URIs in the setting of the application dashboard
REDIRECT_URI = "http://127.0.0.1:5000/api_callback"

SCOPE = 'playlist-modify-private,playlist-modify-public,user-top-read'

# Set this to True for testing but you probably want it set to False in production.
SHOW_DIALOG = True

# authorization-code-flow Step 1. Have your application request authorization;
# the user logs in and authorizes access


@app.route("/")
def verify():
    auth_url = f'{API_BASE}/authorize?client_id={CLI_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'
    print(auth_url)
    return redirect(auth_url)


@app.route("/index")
def index():
    return render_template("index.html")

# authorization-code-flow Step 2.
# Have your application request refresh and access tokens;
# Spotify returns access and refresh tokens


@app.route("/api_callback")
def api_callback():
    session.clear()
    code = request.args.get('code')

    auth_token_url = f"{API_BASE}/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:5000/api_callback",
        "client_id": CLI_ID,
        "client_secret": CLI_SEC
    })

    res_body = res.json()
    print(res.json())
    session["toke"] = res_body.get("access_token")

    return redirect("index")


# authorization-code-flow Step 3.
# Use the access token to access the Spotify Web API;
# Spotify returns requested data
@app.route("/go", methods=['POST'])
def go():
    data = request.form
    sp = spotipy.Spotify(auth=session['toke'])
    response = sp.current_user_top_artists(
        limit=data['num_tracks'], time_range=data['time_range'])
    return render_template("results.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
