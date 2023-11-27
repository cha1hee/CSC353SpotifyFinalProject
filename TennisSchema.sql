DROP SCHEMA IF EXISTS tennishw3;
CREATE SCHEMA tennishw3;
USE tennishw3;

DROP TABLE IF EXISTS player;
CREATE TABLE player
	(id 		INT,
	 name		VARCHAR(33),
	 country	VARCHAR(3),
	 hand		CHAR(1) CONSTRAINT player_check_hand CHECK(hand = 'R' OR hand = 'L' OR hand = 'U' OR hand = 'A'),
	 height		INT CONSTRAINT player_check_height CHECK(height >= 0),
	 PRIMARY KEY (id)
	);

DROP TABLE IF EXISTS tournament;
CREATE TABLE tournament
	(id				VARCHAR(36),
	 name			VARCHAR(40),
	 tourn_level	CHAR(1),
	 tourn_date		DATE,
	 PRIMARY KEY (id)
	);

DROP TABLE IF EXISTS matchinfo;
CREATE TABLE matchinfo
	(match_id		VARCHAR(37),
	 tourney_id		VARCHAR(36),
	 surface		VARCHAR(10),
	 score			VARCHAR(34),
	 num_sets		INT CHECK(num_sets >= 0),
	 rounds			VARCHAR(4),
	 PRIMARY KEY(match_id),
	 FOREIGN KEY (tourney_id) REFERENCES tournament (id) ON DELETE CASCADE
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
