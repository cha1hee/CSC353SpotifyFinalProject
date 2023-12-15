DROP SCHEMA IF EXISTS SpotifyData;
CREATE SCHEMA SpotifyData;
USE SpotifyData;

DROP TABLE IF EXISTS Users;
CREATE TABLE Users
	(username		VARCHAR(33),
	 name			VARCHAR(33),
	 PRIMARY KEY (username)
	);

DROP TABLE IF EXISTS Tracks;
CREATE TABLE Tracks
	(id					VARCHAR(36),
	 title				VARCHAR(60),
	 album				VARCHAR(40),
	 danceability		FLOAT(20, 19),
	 duration			INT,
	 energy				FLOAT,
	 instrumentalness	FLOAT,
	 song_key			INT,
	 liveness			FLOAT,
	 loudness			FLOAT,
	 mode				INT,
	 speechiness		FLOAT,
	 tempo				FLOAT,
	 time_signature		INT,
	 valence			FLOAT,
	 PRIMARY KEY (id)
	);

DROP TABLE IF EXISTS Playlists;
CREATE TABLE Playlists
	(id				VARCHAR(36),
	 playlist_name	VARCHAR(60),
	 username		VARCHAR(33),
	 PRIMARY KEY(id),
	 FOREIGN KEY (username) REFERENCES Users (username)
	);

DROP TABLE IF EXISTS PlaylistTracks;
CREATE TABLE PlaylistTracks
	(playlist_id	VARCHAR(36),
	 track_id		VARCHAR(36),
	 PRIMARY KEY(playlist_id, track_id),
	 FOREIGN KEY (playlist_id) REFERENCES Playlists (id),
	 FOREIGN KEY (track_id) REFERENCES Tracks (id)
	);
