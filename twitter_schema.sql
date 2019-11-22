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
DROP TABLE REQUEST;
DROP TABLE RESEARCHERS;
DROP TABLE PLACE;
DROP TABLE MEDIA;
DROP TABLE USER_MENTION;
DROP TABLE REPLY;

CREATE TABLE RESEARCHERS (
    id    INT,
    full_name  VARCHAR(60) NOT NULL,
    profile    TEXT,
    twitterHandle varchar(60),
    PRIMARY KEY(id)
);

/* INSERT INTO RESEARCHERS VALUES (1, 'Roberto Alejandro Treviño Lozano',
                  'Databases Teacher at Tec'); */

Insert Into Researchers VALUES (1,'Luis Fernando Lomelín Ibarra','DB Student @ ITESM','@LuisLomelín');

CREATE TABLE REQUEST (
    id            INT,
    description   TEXT,
    researcher_id INT,
    PRIMARY KEY(id),
    FOREIGN KEY(researcher_id) references RESEARCHERS(id)
);

/*INSERT INTO REQUEST VALUES(1, 'Search tweets containing top universities', 1);
*/
CREATE TABLE USERS (
    id              BIGINT,
    userhandle      varchar(100),
    username        varchar(100),
    verified        BIT,
    followers_count BIGINT,
    PRIMARY KEY(id)
);


CREATE TABLE TWEETS (
    id                BIGINT,
    userId          BIGINT,
    RequestId         INT,
    "text"            TEXT,
    retweetedNum      BIGINT,
    favoritedNum      BIGINT,
    "language"        varchar(10),
    DOP               text,
    locationId        bigint
    
    
    PRIMARY KEY(id),
    FOREIGN KEY(userId) references USERS(id),
    FOREIGN KEY(RequestId) references REQUEST(id),
    FOREIGN key(locationId) references PLACE(id)
);

CREATE TABLE MEDIA(
    "url" text,
    tweetid bigint,
    PRIMARY KEY ("url"),
    PRIMARY KEY (tweetid),
    FOREIGN KEY (tweetid) REFERENCES TWEETS(id)
);

CREATE TABLE USER_MENTION(
    tweetID BIGINT,
    mentionedUser varchar(100),
    PRIMARY KEY(tweetID),
    PRIMARY KEY(mentionedUser),
    FOREIGN KEY(tweetID) REFERENCES TWWETS(id)

);

CREATE TABLE REPLY(
    tweetID BIGINT,
    userID BIGINT,
    "text" text,
    PRIMARY KEY(tweetID),
    PRIMARY KEY(userID),
    FOREIGN KEY(tweetID) REFERENCES TWWETS(id),
    FOREIGN KEY(userID) REFERENCES USERS(id)
);

CREATE TABLE HASHTAGS (
    tweet_id    BIGINT,
    hashtag     VARCHAR(280),
    PRIMARY KEY(tweet_id, hashtag),
    FOREIGN KEY(tweet_id) references TWEETS(id),
);