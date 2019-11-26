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
    studentId VARCHAR(9),
    profile    TEXT,
    twitterHandle varchar(60),
    PRIMARY KEY(id)
);

/* INSERT INTO RESEARCHERS VALUES (1, 'Roberto Alejandro Treviño Lozano',
                  'Databases Teacher at Tec'); */

Insert Into Researchers VALUES (1,'Luis Fernando Lomelín Ibarra','A01177015','DB Student @ ITESM','@IbarraLomelin');
insert into Researchers VALUES (2,'Arturo Manrique Garza','a01282767' ,'Alumno de ITC 5to semestre', '@ArturoManrique_');
insert into Researchers VALUES (3,'Julio César Gutiérrez Briones','A01282575' ,'Estudiante y Desarrollador de software', '@JulioA01282575');
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

CREATE TABLE PLACE (
	id				BIGINT auto_increment,
    name			TEXT,
    granularity		TEXT,
    latitude		float,
    longitude		float,
    PRIMARY KEY(id)

);
alter table place auto_increment=0;

CREATE TABLE TWEETS (
    id                BIGINT,
    userId          BIGINT,
    RequestId         INT,
    text            TEXT,
    retweetedNum      BIGINT,
    favoritedNum      BIGINT,
    language        varchar(10),
    DOP               text,
    locationId        bigint,
    PRIMARY KEY(id),
    FOREIGN KEY(userId) references USERS(id),
    FOREIGN KEY(RequestId) references REQUEST(id),
    FOREIGN key(locationId) references PLACE(id)
);

CREATE TABLE MEDIA(
    url varchar(255),
    tweetid bigint,
    PRIMARY KEY (url, tweetid),
    FOREIGN KEY (tweetid) REFERENCES TWEETS(id)
);

CREATE TABLE USER_MENTION(
    tweetID BIGINT,
    mentionedUser varchar(100),
    PRIMARY KEY(tweetID,mentionedUser),
    FOREIGN KEY(tweetID) REFERENCES TWEETS(id)

);

CREATE TABLE HASHTAGS (
    tweet_id    BIGINT,
    hashtag     VARCHAR(280),
    PRIMARY KEY(tweet_id, hashtag),
    FOREIGN KEY(tweet_id) references TWEETS(id)
);