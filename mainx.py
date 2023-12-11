from flask import Flask, render_template, redirect, request, session, make_response, session, redirect, jsonify
import spotipy
import spotipy.util as util
from credentz import *
import requests
import urllib.parse
import mysql.connector
import time
from datetime import datetime, timedelta
import random
import string

app = Flask(__name__)
app.secret_key = ''.join(random.choices(
    string.ascii_uppercase + string.ascii_lowercase, k=5))

CLIENT_ID = 'f25ba6368fd6455c8d0da51c7ad1b0a0'
CLIENT_SECRET = '3fce4b7126f3432195118f66269b34f2'
REDIRECT_URI = 'http://localhost:3000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://accounts.spotify.com'

SCOPE = 'playlist-modify-private,playlist-modify-public,user-top-read'


@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <link
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css"
            rel="stylesheet"
            integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We"
            crossorigin="anonymous"
            />
        </head>
        <body>
            <div class="container">
                <div class="row" style="height: 20px;"></div>
                <div class="row">
                    <div class="col-2"></div>
                    <div class="col-8" style="text-align: center;">
                        <h1>Welcome to Sound Mate Spotify!</h1>
                        <br>
                        <a class="btn btn-primary" href="/login" role="button" style="background-color:green; border-color: green;">Login with Spotify</a>
                    </div>
                </div>
            </div>
        </body>
    </html>
'''


@app.route('/login')
def login():
    # scope = 'user-read-private user-read-email'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': SCOPE,
        'redirect_uri': REDIRECT_URI,
        # default is FALSE, and you don't have to include this param at all.
        # TRUE will force the user to re-login if they navigate back to this page.
        # set this just for debugging/testing purposes
        'show_dialog': True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)


# @app.route("/index")
# def index():
#     return render_template("index.html")

# authorization-code-flow Step 2.
# Have your application request refresh and access tokens;
# Spotify returns access and refresh tokens


@app.route("/callback")
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    # session.clear()
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['token_info'] = ['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + \
            token_info['expires_in']

        return redirect('/display')


# authorization-code-flow Step 3.
# Use the access token to access the Spotify Web API;
# Spotify returns requested data
@app.route("/display", methods=['POST'])
def display():
    if 'access_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    data = request.form
    sp = spotipy.Spotify(auth=session['access_token'])
    connection = mysql.connector.connect(
        user='root', password='', host='localhost', database='SpotifyData')
    cursor = connection.cursor()
    # use sp to request user, playlists, tracks, audio features
    # and then after each request, insert to database
    response = sp.current_user_top_artists(
        limit=data['num_tracks'], time_range=data['time_range'])
    return render_template("display.html")


@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + \
            new_token_info['expires_in']

        return redirect('/display')


if __name__ == "__main__":
    app.run(debug=True)
