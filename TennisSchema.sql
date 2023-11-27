DROP SCHEMA IF EXISTS tennishw3;
CREATE SCHEMA tennishw3;
USE tennishw3;

DROP TABLE IF EXISTS user;
CREATE TABLE user
	(username		VARCHAR(33),
	 name			VARCHAR(33),
	 PRIMARY KEY (username)
	);

DROP TABLE IF EXISTS song;
CREATE TABLE song
	(id				VARCHAR(36),
	 title			VARCHAR(40),
	 artist			VARCHAR(30),
	 album			VARCHAR(30),
	 release_date	DATE,
	 -- all the attributes
	 PRIMARY KEY (id)
	);

DROP TABLE IF EXISTS playlist;
CREATE TABLE playlist
	(id				VARCHAR(36),
	 playlist_name	VARCHAR(36),
	 username		VARCHAR(33),
	 PRIMARY KEY(match_id),
	 FOREIGN KEY (username) REFERENCES user (username) ON DELETE CASCADE
	);

DROP TABLE IF EXISTS plays;
CREATE TABLE plays
	(play_id		VARCHAR(15),
	 match_id		VARCHAR(37),
	 player_id		INT,
	 win_or_lose	CHAR(1) CONSTRAINT plays_check_win CHECK(win_or_lose = 'W' OR win_or_lose = 'L'),
	 ace			INT CONSTRAINT plays_check_nonnegative_ace CHECK(ace >= 0),
	 df				INT CONSTRAINT plays_check_nonnegative_df CHECK (df >= 0),
	 fstIn			INT CONSTRAINT plays_check_nonnegative_fstIn CHECK(fstIn >= 0),
	 first_won		INT CONSTRAINT plays_check_nonnegative_first_won CHECK(first_won >= 0),
	 second_won		INT CONSTRAINT plays_check_nonnegative_second_won CHECK(second_won >= 0),
	 break_points_saved	INT CONSTRAINT plays_check_nonnegative_bp_saved CHECK(break_points_saved >= 0),
	 break_points_faced INT CONSTRAINT plays_check_nonnegative_bp_faced CHECK(break_points_faced >= 0),
	 PRIMARY KEY(play_id),
	 FOREIGN KEY (match_id) REFERENCES matchinfo (match_id) ON DELETE SET NULL,
	 FOREIGN KEY (player_id) REFERENCES player (id) ON DELETE SET NULL
	);
