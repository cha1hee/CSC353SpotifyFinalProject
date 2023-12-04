import requests
import urllib.parse
import random
import string
import json
from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session, render_template

app = Flask(__name__)
# app.secret_key = ''.join(random.choices(
#     string.ascii_uppercase + string.ascii_lowercase, k=5))
app.secret_key = '53d355f8-571a-4590-a310-1f9579440851'

CLIENT_ID = 'f25ba6368fd6455c8d0da51c7ad1b0a0'
CLIENT_SECRET = '3fce4b7126f3432195118f66269b34f2'
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'


@app.route('/')
def index():
    return "Welcome to my Spotify App <a href='/login'>Login with Spotify</a>"


@app.route('/login')
def login():
    scope = 'user-read-private user-read-email'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        # default is FALSE, and you don't have to include this param at all.
        # TRUE will force the user to re-login if they navigate back to this page.
        # set this just for debugging/testing purposes
        'show_dialog': True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)


@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})

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

        return redirect('/playlists')


@app.route('/playlists')
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()

    return jsonify(playlists)


@app.route('/display')
def get_display():
    if 'access_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    tracks = set()

    # playlist_response = requests.get(
    #     API_BASE_URL + 'me/playlists', headers=headers)
    # playlists = playlist_response.json()

    # get playlist ids from the response, then iterate over them and make new requestsss
    # /playlists/{playlist_id}/tracks

    # then for each track (or many at once using get Tracks'?) do
    # /audio-features
    #

    # will it work this way?
    # we will ~likely~ need to find some way to pass the json response into a seperate file
    # and handle the actual parsing of the data & inserting to sql in there.
    # if not, i guess we could do it all in this script?
    playlist_response = get_playlists(headers)
    playlist_dict = json.loads(playlist_response)
    # for item in items (this should iterate over every playlist in the object)
    for playlist in playlist_dict['items']:
        # id = playlist_dict['items]['id']
        # this fn is currently stored in data importer but if this works it would probably make sense to move everything in that file over here
        insertPlaylist(playlist['id'], playlist['name'], username)
        tracks_response = get_tracks(headers, playlist['id'])
        tracks_dict = json.loads(tracks_response)
        for track in tracks_dict['items']:
            insertPlaylistTracks(playlist['id'], track['track']['id'])
            if track['track']['id'] not in tracks:
                audio_features_response = get_audio_features(
                    headers, track['track']['id'])
                audio_features_dict = json.loads(audio_features_response)
                insertTrack(track['track']['id'], track['track']['name'], track['album']['name'], audio_features_dict['danceability'], audio_features_dict['duration_ms'], audio_features_dict['energy'], audio_features_dict['instrumentalness'], audio_features_dict['key'],
                            audio_features_dict['liveness'], audio_features_dict['loudness'], audio_features_dict['mode'], audio_features_dict['speechiness'], audio_features_dict['tempo'], audio_features_dict['time_signature'], audio_features_dict['valence'])

    # tracks_response = get_tracks(headers, playlist_id)
    return render_template('display.html')

    # maybe here, we could return by calling a function/a different script?
    # so we'd be returning the code(?) for the display page/the page users can interact with to see their data
    # or do that before the return??
    # return jsonify(playlists)


def get_playlists(headers):
    response = requests.get(
        API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()
    return jsonify(playlists)


def get_tracks(headers, playlist_id):
    response = requests.get(
        API_BASE_URL + 'playlists/' + playlist_id + '/tracks', headers=headers)
    tracks = response.json()
    return jsonify(tracks)


def get_audio_features(headers, track_id):
    response = requests.get(
        API_BASE_URL + 'audio-features/' + track_id, headers=headers)
    audio_features = response.json()
    return jsonify(audio_features)


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

        return redirect('/playlists')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
