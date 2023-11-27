DROP SCHEMA IF EXISTS spotifydata;
CREATE SCHEMA spotifydata;
USE spotifydata;

DROP TABLE IF EXISTS user;
CREATE TABLE user
	(username		VARCHAR(33),
	 name			VARCHAR(33),
	 PRIMARY KEY (username)
	);

DROP TABLE IF EXISTS song;
CREATE TABLE song
	(id					VARCHAR(36),
	 title				VARCHAR(40),
	 artist				VARCHAR(30),
	 album				VARCHAR(30),
	 release_date		DATE,
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

DROP TABLE IF EXISTS playlist;
CREATE TABLE playlist
	(id				VARCHAR(36),
	 playlist_name	VARCHAR(36),
	 username		VARCHAR(33),
	 PRIMARY KEY(id),
	 FOREIGN KEY (username) REFERENCES user (username) ON DELETE CASCADE
	);

DROP TABLE IF EXISTS playlist_songs;
CREATE TABLE playlist_songs
	(playlist_id	VARCHAR(36),
	 song_id		VARCHAR(36),
	 PRIMARY KEY(playlist_id, song_id),
	 FOREIGN KEY (playlist_id) REFERENCES playlist (id) ON DELETE CASCADE,
	 FOREIGN KEY (song_id) REFERENCES song (id) ON DELETE CASCADE
	);
