import requests
import urllib.parse
import mysql.connector
import random
import string
import json
import time
from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session, render_template

app = Flask(__name__)
app.secret_key = ''.join(random.choices(
    string.ascii_uppercase + string.ascii_lowercase, k=5))

CLIENT_ID = 'f25ba6368fd6455c8d0da51c7ad1b0a0'
CLIENT_SECRET = '3fce4b7126f3432195118f66269b34f2'
REDIRECT_URI = 'http://localhost:3000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'


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

        return redirect('/display')


'''
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
'''


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
    tracks = set()
    # playlists = set()

    # ??????? can we connect here???
    connection = mysql.connector.connect(
        user='root', password='123456', host='localhost', database='SpotifyData')
    cursor = connection.cursor()
    user_response = get_user(headers)
    # with open("userResponse.json", "w") as outfile:
    #     json.dump(user_response, outfile)
    user_dict = json.loads(user_response)
    insertUser(connection, cursor, user_dict['id'], user_dict['display_name'])
    playlist_response = get_playlists(headers)
    playlist_dict = json.loads(playlist_response)
    with open("playlistResponse.json", "w") as outfile:
        json.dump(playlist_response, outfile)
    # for each playlist id, request every track on that playlist
    # for playlist in playlist_response['items']:
    #     tracks_response = get_tracks(headers, playlist['id'])
    #     with open("tracksResponse.json", "w") as outfile:
    #         json.dump(tracks_response, outfile)

    # playlist_dict = json.loads(playlist_response)
    # for item in items (this should iterate over every playlist in the object)
    for playlist in playlist_dict['items']:
        # id = playlist_dict['items]['id']
        # this fn is currently stored in data importer but if this works it would probably make sense to move everything in that file over here
        insertPlaylist(connection, cursor, playlist['id'],
                       playlist['name'], user_dict['id'])
        tracks_response = get_tracks(headers, playlist['id'])
        tracks_dict = json.loads(tracks_response)
        for track in tracks_dict['items']:
            # wait until we have 100 tracks, and then use the Get Tracks' Audio Features endpoint!
            if track['track']['id'] not in tracks:
                audio_features_response = get_audio_features(
                    headers, track['track']['id'])
                audio_features_dict = json.loads(audio_features_response)
                insertTrack(connection, cursor, track['track']['id'], track['track']['name'], track['track']['album']['name'], audio_features_dict['danceability'], audio_features_dict['duration_ms'], audio_features_dict['energy'], audio_features_dict['instrumentalness'], audio_features_dict['key'],
                            audio_features_dict['liveness'], audio_features_dict['loudness'], audio_features_dict['mode'], audio_features_dict['speechiness'], audio_features_dict['tempo'], audio_features_dict['time_signature'], audio_features_dict['valence'])
                tracks.add(track['track']['id'])
            insertPlaylistTracks(connection, cursor,
                                 playlist['id'], track['track']['id'])
    cursor.close()
    return render_template('display.html')


# tracks_response = get_tracks(headers, playlist_id)
# return render_template('display.html')

# maybe here, we could return by calling a function/a different script?
# so we'd be returning the code(?) for the display page/the page users can interact with to see their data
# or do that before the return??


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


def get_user(headers):
    response = requests.get(
        API_BASE_URL + 'me', headers=headers)
    user = response.json()
    return json.dumps(user)


def get_playlists(headers):
    response = requests.get(
        API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()
    return json.dumps(playlists)


def get_tracks(headers, playlist_id):
    # how can we use limit & offset to get ALL items?
    response = requests.get(
        API_BASE_URL + 'playlists/' + playlist_id + '/tracks?limit=50', headers=headers)
    tracks = response.json()
    return json.dumps(tracks)


def get_audio_features(headers, track_id):
    response = requests.get(
        API_BASE_URL + 'audio-features/' + track_id, headers=headers)
    audio_features = response.json()
    return json.dumps(audio_features)


def insertUser(connection, cursor, username, name):
    query_string = "INSERT INTO Users VALUES (%s, %s)"
    try:
        cursor.execute(query_string, (username, name))
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))


def insertPlaylist(connection, cursor, id, name, username):
    query_string = "INSERT INTO Playlists VALUES (%s, %s, %s)"
    try:
        cursor.execute(query_string, (id, name, username))
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))
        print("failed on insertPlaylist: id: " + id + " name: " + name)

# not done this one

# save everything into a file!!!! then import the data from that file
# also pick only the relevant attributes probably
# maybe try 2 accounts


def insertPlaylistTracks(connection, cursor, playlist_id, track_id):
    query_string = "INSERT INTO PlaylistTracks VALUES (%s, %s)"
    try:
        cursor.execute(query_string, (playlist_id, track_id))
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))
        print("failed on insertPlaylistTrack: playlist_id: " +
              playlist_id + " track_id: " + track_id)


def insertTrack(connection, cursor, id, title, album, danceability, duration, energy, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, time_signature, valence):
    query_string = "INSERT INTO Tracks VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(query_string, (id, title, album, danceability, duration, energy, instrumentalness,
                       key, liveness, loudness, mode, speechiness, tempo, time_signature, valence))
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))
        print("failed on insertTrack: id: " + id + " title: " + title)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
