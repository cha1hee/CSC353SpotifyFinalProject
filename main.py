from flask import Flask, render_template, redirect, request, session, make_response, session, redirect, jsonify
import spotipy
import spotipy.util as util
import requests
import urllib.parse
import mysql.connector
from datetime import datetime
import random
import string
import json
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = ''.join(random.choices(
    string.ascii_uppercase + string.ascii_lowercase, k=5))

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:3000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://accounts.spotify.com'

SCOPE = 'playlist-read-private,playlist-read-collaborative,user-read-private'

TRACK_INFO_INDEX = 0
TRACK_FEATURES_INDEX = 1

USERS_USERNAME_MAX_LENGTH = 33
USERS_NAME_MAX_LENGTH = 33
PLAYLISTS_ID_MAX_LENGTH = 36
PLAYLISTS_NAME_MAX_LENGTH = 90
TRACKS_ID_MAX_LENGTH = 36
TRACKS_TITLE_MAX_LENGTH = 90
TRACKS_ALBUM_MAX_LENGTH = 80


# class User:
#     def __init__(self, username, display_name):
#         self.username = username
#         self.display_name = display_name


# class Playlist:
#     tracks = set()

#     def __init__(self, playlist_id, name, username):
#         self.playlist_id = playlist_id
#         self.name = name
#         self.username = username


# class Track:
#     on_playlists = set()
#     title = str
#     album = str
#     inserted = False
#     audio_features = dict()

#     def __init__(self, track_id):
#         self.track_id = track_id


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


@app.route("/callback")
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

        return render_template('provideUsername.html')

# add try-except blocks for inserting playlists, tracks, and playlist tracks
# also wrap the api requests in if-statement checking that the id is not already in the database – it shouldn't be, but whatever


@app.route("/display", methods=['POST'])
def get_display():
    if 'access_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    sp = spotipy.Spotify(auth=session['access_token'])

    provided_user_id = request.form.get('username')

    # exec(open('setupSchema.py').read())

    connection = mysql.connector.connect(
        user='root', password='123456', host='localhost', database='SpotifyData')
    cursor = connection.cursor()
    # # use sp to request user, playlists, tracks, audio features
    # # and then after each request, insert to database
    # inserted_users = set()
    # inserted_playlists = set()
    # inserted_tracks = set()
    # playlist_dropdown_items = {'All Tracks': 'all-tracks'}
    # # user = None
    # # playlists = None
    # # playlist_tracks = None
    # # tracks_audio_features = None

    # try:
    #     # user = sp.current_user()
    #     user = sp.user(provided_user_id)
    # except spotipy.SpotifyException as error:
    #     handle_sp_exception(error)
    # if (user is not None) and (user['id'] not in inserted_users):
    #     insert_user(inserted_users, connection, cursor,
    #                 user['id'], user['display_name'])
    # try:
    #     playlists = get_all_playlists(sp, provided_user_id)
    # except spotipy.SpotifyException as error:
    #     handle_sp_exception(error)
    # for playlist in playlists:
    #     if (playlist is not None) and (playlist['id'] not in inserted_playlists):
    #         insert_playlist(inserted_playlists, connection, cursor,
    #                         playlist['id'], playlist['name'], user['id'])
    #         playlist_dropdown_items[playlist['name']] = playlist['id']
    #     current_playlist_tracks = set()
    #     # get all tracks from the playlist
    #     try:
    #         playlist_tracks = get_all_playlist_tracks(
    #             sp, user['id'], playlist['id'])
    #     except spotipy.SpotifyException as error:
    #         handle_sp_exception(error)
    #     tracks_to_request = dict()
    #     for track in playlist_tracks:
    #         if (track['track'] is None):
    #             break
    #         # if track is not in database, add it to the set storing track ids in current playlist
    #         # add its information to tracks_to_request
    #         if track['track']['id'] not in inserted_tracks:
    #             current_playlist_tracks.add(track['track']['id'])
    #             track_info = dict(
    #                 title=track['track']['name'], album=track['track']['album']['name'])
    #             track_data = [track_info]
    #             tracks_to_request[track['track']['id']] = track_data
    #             # if we've hit the limit of 100 tracks, or if we've gotten through all tracks in the playlist, call API
    #             # extract the IDs of the next 100 tracks to request from API
    #             # after response, add audio features for each track to tracks_to_request
    #             if len(tracks_to_request) == 100 or len(current_playlist_tracks) == playlist['tracks']['total']:
    #                 track_ids = tracks_to_request.keys()
    #                 try:
    #                     tracks_audio_features = sp.audio_features(track_ids)
    #                 except spotipy.SpotifyException as error:
    #                     print(error)
    #                     handle_sp_exception(error)
    #                 for key, value, track_features in zip(tracks_to_request.keys(), tracks_to_request.values(), tracks_audio_features):
    #                     value.extend([track_features])
    #                 for key in tracks_to_request:
    #                     insert_track(inserted_tracks, connection, cursor, key, tracks_to_request[key][TRACK_INFO_INDEX]['title'], tracks_to_request[key][TRACK_INFO_INDEX]['album'], tracks_to_request[key][TRACK_FEATURES_INDEX]['danceability'], tracks_to_request[key][TRACK_FEATURES_INDEX]['duration_ms'], tracks_to_request[key][TRACK_FEATURES_INDEX]['energy'],
    #                                  tracks_to_request[key][TRACK_FEATURES_INDEX]['instrumentalness'], tracks_to_request[key][TRACK_FEATURES_INDEX]['key'], tracks_to_request[key][TRACK_FEATURES_INDEX]['liveness'], tracks_to_request[key][TRACK_FEATURES_INDEX]['loudness'], tracks_to_request[key][TRACK_FEATURES_INDEX]['mode'], tracks_to_request[key][TRACK_FEATURES_INDEX]['speechiness'], tracks_to_request[key][TRACK_FEATURES_INDEX]['tempo'], tracks_to_request[key][TRACK_FEATURES_INDEX]['time_signature'], tracks_to_request[key][TRACK_FEATURES_INDEX]['valence'])
    #                     insert_playlist_tracks(connection, cursor,
    #                                            playlist['id'], key)
    #                 tracks_to_request = dict()
    #         # if current track HAS been inserted to Tracks from a previous playlist, add new relationship to current playlist
    #         # and add it to set of current playlist tracks
    #         elif track['track']['id'] not in current_playlist_tracks:
    #             current_playlist_tracks.add(track['track']['id'])
    #             insert_playlist_tracks(connection, cursor,
    #                                    playlist['id'], track['track']['id'])
    # cursor.close()
    # connection.close()
    # json_playlist_dropdown_items = json.dumps(playlist_dropdown_items)
    playlist_dropdown_items = {'All Tracks': 'all-tracks'}
    playlist_options_result = query_playlist_names_for_dropdown()
    playlist_dropdown_items.update(playlist_options_result)
    json_playlist_dropdown_items = json.dumps(playlist_dropdown_items)
    cursor.close()
    connection.close()
    return render_template("display.html", json_playlist_dropdown_items=json_playlist_dropdown_items, json_audio_data=None)


@app.route('/query', methods=['POST'])
def query():
    playlist_dropdown_items = {'All Tracks': 'all-tracks'}
    playlist_options_result = query_playlist_names_for_dropdown()
    playlist_dropdown_items.update(playlist_options_result)
    json_playlist_dropdown_items = json.dumps(playlist_dropdown_items)
    playlist_id = request.form.get('selected-value')
    if (playlist_id == 'all-tracks'):
        query_result = query_all_tracks_features()
    else:
        query_result = query_playlist_tracks_features(playlist_id)
    query_result_list = list(query_result[0])
    json_audio_data = json.dumps(query_result_list)
    return render_template('display.html', json_playlist_dropdown_items=json_playlist_dropdown_items, json_audio_data=json_audio_data)


def query_playlist_names_for_dropdown():
    connection = mysql.connector.connect(
        user='root', password='123456', host='localhost', database='SpotifyData')
    cursor = connection.cursor()
    query_string = "SELECT playlist_name, id FROM Playlists;"
    cursor.execute(query_string)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return dict(result)


def query_playlist_tracks_features(playlist_id):
    connection = mysql.connector.connect(
        user='root', password='123456', host='localhost', database='SpotifyData')
    cursor = connection.cursor()
    query_params = []
    query_params.append(playlist_id)
    query_string = "SELECT AVG(Tracks.danceability),AVG(Tracks.valence), AVG(Tracks.liveness), AVG(Tracks.energy), AVG(Tracks.speechiness) FROM (PlaylistTracks, Tracks, Playlists) WHERE track_id = Tracks.id AND playlist_id = Playlists.id AND playlist_id = (%s) GROUP BY playlist_id;"
    cursor.execute(query_string, (query_params))
    # QUERY GOES HERE – FORMATTED THE WAY WE WANT
    # fetchall returns a list of tuples
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def query_all_tracks_features():
    connection = mysql.connector.connect(
        user='root', password='123456', host='localhost', database='SpotifyData')
    cursor = connection.cursor()
    query_string = "SELECT AVG(Tracks.danceability),AVG(Tracks.valence), AVG(Tracks.liveness), AVG(Tracks.energy), AVG(Tracks.speechiness) FROM Tracks;"
    cursor.execute(query_string)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


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

        return render_template('provideUsername.html')


def get_all_playlists(sp, user_id):
    results = sp.user_playlists(user_id)
    playlists = results['items']
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])
    return playlists


def get_all_playlist_tracks(sp, username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


def handle_sp_exception(error):
    error_message = ''
    if error.http_status == 401:
        error_message = "Authentication error. Check your credentials."
    elif error.http_status == 429:
        error_message = "Rate limit exceeded. Wait and try again later."
    else:
        error_message = f"An unexpected SpotifyException occured: {error}"
    return render_template('errorPage.html', error_message=error_message)


def insert_user(inserted_users, connection, cursor, username, name):
    query_string = "INSERT INTO Users VALUES (%s, %s)"
    fit_username = fit_string_before_insert(
        username, USERS_USERNAME_MAX_LENGTH)
    fit_name = fit_string_before_insert(name, USERS_NAME_MAX_LENGTH)
    try:
        cursor.execute(query_string, (fit_username, fit_name))
        connection.commit()
        inserted_users.add(username)
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))


def insert_playlist(inserted_playlists, connection, cursor, id, name, username):
    query_string = "INSERT INTO Playlists VALUES (%s, %s, %s)"
    fit_id = fit_string_before_insert(id, PLAYLISTS_ID_MAX_LENGTH)
    fit_name = fit_string_before_insert(name, PLAYLISTS_NAME_MAX_LENGTH)
    try:
        cursor.execute(query_string, (fit_id, fit_name, username))
        connection.commit()
        inserted_playlists.add(id)
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))


def insert_playlist_tracks(connection, cursor, playlist_id, track_id):
    query_string = "INSERT INTO PlaylistTracks VALUES (%s, %s)"
    try:
        cursor.execute(query_string, (playlist_id, track_id))
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))


def insert_track(inserted_tracks, connection, cursor, id, title, album, danceability, duration, energy, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, time_signature, valence):
    query_string = "INSERT INTO Tracks VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    fit_id = fit_string_before_insert(id, TRACKS_ID_MAX_LENGTH)
    fit_title = fit_string_before_insert(title, TRACKS_TITLE_MAX_LENGTH)
    fit_album = fit_string_before_insert(album, TRACKS_ALBUM_MAX_LENGTH)
    try:
        cursor.execute(query_string, (fit_id, fit_title, fit_album, danceability, duration, energy, instrumentalness,
                       key, liveness, loudness, mode, speechiness, tempo, time_signature, valence))
        connection.commit()
        inserted_tracks.add(id)
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))
        print("album length: ", len(album), " && title len: ", len(title))


def fit_string_before_insert(str, max_length):
    fit_str = (str[:max_length - 2] +
               '..') if len(str) > max_length else str
    return fit_str


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
