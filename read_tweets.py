#!/usr/bin/python

import tweepy
import json
import time
import sys
import glob
import mysql.connector

config = {
    'user': 'root',
        'password': '',
            'host': '127.0.0.1',
                'database': 'TwitterProject',
                    'raise_on_warnings': True
}

conn = mysql.connector.connect(**config)
#conn = mysql.connector.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+password)
cursor = conn.cursor()
cursor.execute('SELECT * FROM RESEARCHERS')

for row in cursor:
    print(row)

# read all json files
file_str = r'bdatweets_*.json'
# list of pathnames according to above regex
file_lst = glob.glob(file_str)

# process every file
for file_idx, file_name in enumerate(file_lst):
    counter = 0
    placeCount = 0
    with open(file_name, 'r') as f:
        for line in f:
            if counter == 0:
				# read researcher ID from the first line
                researcherID = int(line)
                counter = counter + 1
                continue
            if counter == 1:
				# read search ID from the second line
                searchID = int(line)
                counter = counter + 1
                continue
            if line != '\n':
				# each line is a tweet json object, load it and display user id
                tweet = json.loads(line)
				# user info
                userID = int(tweet['user']['id'])
                verified = tweet['user']['verified']
                followers_count = tweet['user']['followers_count']
                userhandle= tweet['user']['screen_name']
                username = tweet['user']['name']
				# tweet info
                tweet_id = tweet['id']
                tweet_text = tweet['text']
                favorite_count = int(tweet['favorite_count'])
                retweetNum= int(tweet['retweet_count'])
                lang=tweet['lang']
                dayOfp=tweet['created_at']
				# read hashtag information [indices, text]
				# Place info
                print(tweet['coordinates'])
				# end of place info
                userMentions_obj= tweet['entities']['user_mentions']
				# Media info
                #media_obj=tweet['entities']['media']
				# end of media info
                hashtag_objects = tweet['entities']['hashtags']
				# insert only if the user doesn't exists already in the database
                print(userID)
                rows = cursor.execute('SELECT * FROM USERS WHERE id = ?', userID).fetchall()
                if len(rows) == 0:
                    cursor.execute('''
                        INSERT INTO USERS (id, verified, followers_count)
                            VALUES
                                (?,?,?,?,?)
                    ''', (userID, userhandle, username, verified, followers_count))
                    conn.commit()
				# insert tweet object
                cursor.execute('''
					INSERT INTO TWEETS (id, userId, requestId, text, retweetNum, favoriteNum, lang, DOP, locationId, search_id)
                        VALUES
                            (?,?,?,?,?,?,?,?,?)
				''', (tweet_id, userID,  userID, tweet_text,retweetNum,favorite_count, lang, dayOfp, null, favorite_count, searchID))
                conn.commit()
				# insert hashtags
                for hashtag in hashtag_objects:
					# insert only unique hashtags
                    rows = cursor.execute('''SELECT * FROM HASHTAGS WHERE tweet_id = ? AND
                        hashtag = ?''', (tweet_id, hashtag['text'])).fetchall()
                    if len(rows) == 0:
                        cursor.execute('''
                            INSERT INTO HASHTAGS (tweet_id, hashtag)
                                VALUES(?,?)
                        ''', (tweet_id, hashtag['text']))
                        conn.commit()
                # insert places
                if tweet['coordinates'] != 'none':
                    latitude = float(tweet['coordinates'][1])
                    longitude = float(tweet['coordinates'][2])
                    placeCount = placeCount + 1 
                    granularity = ''
                    name=tweet['place']['country']+" "+ tweet['place']['full_name']
                    rows = cursor.execute('''SELECT * FROM PLACE WHERE 
                        name = ?''', (name)).fetchall()
                    if len(rows) == 0:
                        cursor.execute('''
                            INSERT INTO PLACE (id,name,granularity,latitude,longitude)
                                VALUES(?,?,?,?,?)
                        ''', (placeCount, name, granularity, latitude, longitude ))
                        conn.commit()
                for media in media_obj:
                    rows = cursor.execute(''' SELECT * FROM MEDIA WHERE url = ? and tweetid = ?''',(media['display_url'],tweet_id)).fetchcall()
                    if len(rows) == 0:
                        cursor.execute(''' INSERT INTO MEDIA (url,tweetid) VALUES(?,?)''',(media['display_url'],tweet_id))
                        conn.commit()
                for mention in userMentions_obj:
                    rows = cursor.execute(''' SELECT * FROM USER_MENTION WHERE mentionedUser = ? and tweetid = ?''',(mention['screen_name'],tweet_id)).fetchcall()
                    if len(rows) == 0:
                        cursor.execute(''' INSERT INTO USER_MENTION (mentionedUser,tweetid) VALUES(?,?)''',(mention['screen_name'],tweet_id))
                        conn.commit()
                if tweet['in_reply_to_status_id'] != null:
                    rows = cursor.execute(''' SELECT * FROM REPLY WHERE userId = ? and tweetid = ?''',(tweet['user']['id'],tweet['in_reply_to_status_id'])).fetchcall()
                    if len(rows) == 0:
                        cursor.execute(''' INSERT INTO REPLY (userId,tweetid) VALUES(?,?)''',(tweet['user']['id'],tweet['in_reply_to_status_id']))
                        conn.commit()
cursor.close()
conn.close()
