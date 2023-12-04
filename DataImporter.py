# Kate Hynes and Pauline Cha

# Install with pip install mysql-connector-python (on some systems 'pip' might be called 'pip3')
import mysql.connector
import os
import glob
import csv
import datetime
import calendar

TOURNEY_ID = 0
TOURNEY_NAME = 1
SURFACE = 2
DRAW_SIZE = 3
TOURNEY_LEVEL = 4
TOURNEY_DATE = 5
MATCH_NUM = 6
WINNER_ID = 7
WINNER_NAME = 10
WINNER_HAND = 11
WINNER_HT = 12
WINNER_IOC = 13
LOSER_ID = 15
LOSER_NAME = 18
LOSER_HAND = 19
LOSER_HT = 20
LOSER_IOC = 21
SCORE = 23
BEST_OF = 24
ROUND = 25
W_ACE = 27
W_DF = 28
W_1STIN = 30
W_1STWON = 31
W_2NDWON = 32
W_BPSAVED = 34
W_BPFACED = 35
L_ACE = 36
L_DF = 37
L_1STIN = 39
L_1STWON = 40
L_2NDWON = 41
L_BPSAVED = 43
L_BPFACED = 44

# Connect to MySQL
connection = mysql.connector.connect(
    user='root', password='123456', host='localhost', database='tennishw3')
cursor = connection.cursor()

# sets to store new IDs for each entity
players = set()
matches = set()
tourneys = set()
plays = set()

# ??
user_ids = set()
playlist_ids = set()
track_ids = set()

# ??


def parsePlaylistData(response):
    username = response['username']
    # get the id of each playlist & the name
    # and call insertPlaylist
    # for each playlist in json object
    playlist_id = response['id']
    playlist_name = response['name']

    insertPlaylist(playlist_id, playlist_name, username)
    ##


def connectToDatabase():
    connection = mysql.connector.connect(
        user='root', password='123456', host='localhost', database='tennishw3')
    cursor = connection.cursor()


def insertPlaylist(id, name, username):
    query_string = "INSERT INTO playlist VALUES (%s, %s, %s)"
    try:
        cursor.execute(query_string, (id, name, username))
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))

# not done this one


def insertPlaylistTracks(playlist_id, track_id):
    query_string = "INSERT INTO playlisttracks VALUES (%s, %s)"
    try:
        cursor.execute(query_string, (playlist_id, track_id))
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))


def insertTrack(id, title, album, danceability, duration, energy, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, time_signature, valence):
    query_string = "INSERT INTO tracks VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(query_string, (id, title, album, danceability, duration, energy, instrumentalness,
                       key, liveness, loudness, mode, speechiness, tempo, time_signature, valence))
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))

####


def convertDate(date):
    year = date[0:4]
    month = calendar.month_name[int(date[4:6])] + ' '
    day = date[6:8] + ' '
    formatted_date = month + day + year
    return datetime.datetime.strptime(formatted_date, '%B %d %Y').strftime('%Y-%m-%d')


def insertPlayer(id, name, country, hand, height):
    query_string = "INSERT INTO player VALUES (%s, %s, %s, %s, %s)"
    if name == '':
        name = None
    if country == '':
        country = None
    if hand == '':
        hand = None
    if height == '':
        height = None
    try:
        cursor.execute(query_string, (id, name, country, hand, height))
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))


def insertTourney(id, name, level, date):
    query_string = "INSERT INTO tournament VALUES (%s, %s, %s, %s)"
    if name == '':
        name = None
    if level == '':
        level = None
    if date == '':
        date = None
    else:
        date = convertDate(date)
    try:
        cursor.execute(query_string, (id, name, level, date))
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))


def insertMatchInfo(match_id, tourney_id, surface, score, num_sets, rounds):
    query_string = "INSERT INTO matchinfo VALUES (%s, %s, %s, %s, %s, %s)"
    if tourney_id == '':
        tourney_id = None
    if surface == '':
        surface = None
    if score == '':
        score = None
    if num_sets == '':
        num_sets = None
    if rounds == '':
        rounds = None
    try:
        cursor.execute(query_string, (match_id, tourney_id,
                                      surface, score, num_sets, rounds))
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))


def insertPlays(plays_id, match_id, player_id, win_or_lose, ace, df, fstIn, first_won, second_won, break_points_saved, break_points_faced):
    query_string = "INSERT INTO plays VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    if win_or_lose == '':
        win_or_lose = None
    if ace == '':
        ace = None
    if df == '':
        df = None
    if fstIn == '':
        fstIn = None
    if first_won == '':
        first_won = None
    if second_won == '':
        second_won = None
    if break_points_saved == '':
        break_points_saved = None
    if break_points_faced == '':
        break_points_faced = None
    try:
        cursor.execute(query_string, (plays_id, match_id, player_id,
                                      win_or_lose, ace, df, fstIn, first_won, second_won, break_points_saved, break_points_faced))
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tuple: {}".format(error_descriptor))


# for all the files in the csv directory
for filename in glob.glob("tennis_atp-master/*.csv"):
    file = open(filename)
    csvreader = csv.reader(file)
    i = 0
    for row in csvreader:
        if i != 0:
            # Player
            winner_id = row[WINNER_ID]
            if (winner_id not in players):
                insertPlayer(winner_id, row[WINNER_NAME], row[WINNER_IOC],
                             row[WINNER_HAND], row[WINNER_HT])
                players.add(winner_id)
            loser_id = row[LOSER_ID]
            if (loser_id not in players):
                insertPlayer(loser_id, row[LOSER_NAME], row[LOSER_IOC],
                             row[LOSER_HAND], row[LOSER_HT])
                players.add(loser_id)
            # Tourney
            tourney_id = row[TOURNEY_ID]
            if (tourney_id not in tourneys):
                insertTourney(tourney_id, row[TOURNEY_NAME],
                              row[TOURNEY_LEVEL], row[TOURNEY_DATE])
                tourneys.add(tourney_id)
            # Matches
            match_id = tourney_id + '-' + row[MATCH_NUM]
            if (match_id not in matches):
                insertMatchInfo(
                    match_id, tourney_id, row[SURFACE], row[SCORE], row[BEST_OF], row[ROUND])
                matches.add(match_id)
            # Plays
            w_plays_key = len(plays)+1
            if (w_plays_key not in plays):
                insertPlays(w_plays_key, match_id, winner_id, 'W',
                            row[W_ACE], row[W_DF], row[W_1STIN], row[W_1STWON], row[W_2NDWON], row[W_BPSAVED], row[W_BPFACED])
                plays.add(w_plays_key)
            l_plays_key = len(plays)+1
            if (l_plays_key not in plays):
                insertPlays(l_plays_key, match_id, loser_id, 'L',
                            row[L_ACE], row[L_DF], row[L_1STIN], row[L_1STWON], row[L_2NDWON], row[L_BPSAVED], row[L_BPFACED])
                plays.add(l_plays_key)
        i += 1
    connection.commit()
    file.close()
cursor.close()
