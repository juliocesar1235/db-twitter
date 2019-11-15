SET NOCOUNT ON
GO

USE master
GO
if exists (select * from sysdatabases where name='TwitterProject')
		drop database TwitterProject
GO

CREATE DATABASE TwitterProject;
GO

use TwitterProject
GO

DROP TABLE HASHTAGS;
DROP TABLE TWEETS;
DROP TABLE USERS;
DROP TABLE SEARCHES;
DROP TABLE RESEARCHERS;

CREATE TABLE RESEARCHERS (
    id    INT,
    full_name  VARCHAR(60) NOT NULL,
    profile    TEXT,
    PRIMARY KEY(id)
);

INSERT INTO RESEARCHERS VALUES (1, 'Roberto Alejandro Treviño Lozano',
                  'Databases Teacher at Tec');

CREATE TABLE SEARCHES (
    id            INT,
    description   TEXT,
    researcher_id INT,
    PRIMARY KEY(id),
    FOREIGN KEY(researcher_id) references RESEARCHERS(id)
);

INSERT INTO SEARCHES VALUES(1, 'Search tweets containing top universities', 1);

CREATE TABLE USERS (
    id              BIGINT,
    verified        BIT,
    followers_count BIGINT,
    PRIMARY KEY(id)
);

CREATE TABLE TWEETS (
    id                BIGINT,
    tweet_text        TEXT,
    "user"            BIGINT,
    favorite_count    BIGINT,
    search_id         INT,
    PRIMARY KEY(id),
    FOREIGN KEY("user") references USERS(id),
    FOREIGN KEY(search_id) references SEARCHES(id)
);

CREATE TABLE HASHTAGS (
    tweet_id    BIGINT,
    hashtag     VARCHAR(280),
    PRIMARY KEY(tweet_id, hashtag),
    FOREIGN KEY(tweet_id) references TWEETS(id),
);