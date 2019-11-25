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
                    'raise_on_warnings': True,
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
                placeId=None;
				# read hashtag information [indices, text]
				# Place info
                print(tweet['coordinates']['type'])
                if tweet['coordinates'] != None:
                    latitude = float(tweet['coordinates']['cooridinates'][0])
                    longitude = float(tweet['coordinates']['cooridinates'][1])
                    granularity = tweet['coordinates']['type']
                    name=tweet['place']['country']+" "+ tweet['place']['full_name']
                    rows = cursor.execute('''SELECT * FROM PLACE WHERE 
                        latitude = %s and longitude= %s''', (latitude,longitude,)).fetchall()
                    if len(rows) == 0:
                        placeCount = placeCount + 1 
                        cursor.execute('''
                            INSERT INTO PLACE (id,name,granularity,latitude,longitude)
                                VALUES(%s,%s,%s,%s,%s)
                        ''', (placeCount, name, granularity, latitude, longitude, ))
                        placeId=placeCount
				# end of place info
                userMentions_obj= tweet['entities']['user_mentions']
				# Media info
                #media_obj=tweet['entities']['media']
				# end of media info
                hashtag_objects = tweet['entities']['hashtags']
				# insert only if the user doesn't exists already in the database
                print(userID)
                statement=('SELECT * FROM USERS WHERE id = %s')
                value=(userID,)
                cursor.execute(statement, value)
                rows = cursor.fetchall()
                if len(rows) == 0:
                    cursor.execute('''
                        INSERT INTO USERS (id, userhandle, username, verified, followers_count)
                            VALUES
                                (%s,%s,%s,%s,%s)
                    ''', (userID, userhandle, username, verified, followers_count))
                    conn.commit()
				# insert tweet object
                statement=('SELECT * FROM TWEETS WHERE id = %s')
                value=(tweet_id,)
                cursor.execute(statement, value)
                rows= cursor.fetchall()
                if len(row) == 0:
                    cursor.execute('''
                        INSERT INTO TWEETS (id, userId, requestId, text, retweetedNum, favoritedNum, language, DOP, locationId)
                            VALUES
                                (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ''', (tweet_id, userID,  None, tweet_text,retweetNum,favorite_count, lang, dayOfp, placeId,))
                    conn.commit()
                    # insert hashtags
                    for hashtag in hashtag_objects:
                        # insert only unique hashtags
                        statement=("SELECT * FROM HASHTAGS WHERE tweet_id = %s AND"
                            "hashtag = %s")
                        value= (tweet_id, hashtag['text'],)
                        cursor.execute(statement,value)
                        rows = cursor.fetchall()
                        if len(rows) == 0:
                            cursor.execute('''
                                INSERT INTO HASHTAGS (tweet_id, hashtag)
                                    VALUES(%s,%s)
                            ''', (tweet_id, hashtag['text'],))
                            conn.commit()
                    # insert places
                    if 'media' in tweet['entities']:
                        media_obj=tweet['entities']['media']
                        for media in media_obj:
                            cursor.execute(''' SELECT * FROM MEDIA WHERE url = %s and tweetid = %s''',(media['display_url'],tweet_id,))
                            rows = cursor.fetchcall()
                            if len(rows) == 0:
                                cursor.execute(''' INSERT INTO MEDIA (url,tweetid) VALUES(%s,%s)''',(media['display_url'],tweet_id,))
                                conn.commit()
                    for mention in userMentions_obj:
                        cursor.execute(''' SELECT * FROM USER_MENTION WHERE mentionedUser = %s and tweetid = %s''',(mention['screen_name'],tweet_id,))
                        rows = cursor.fetchcall()
                        if len(rows) == 0:
                            cursor.execute(''' INSERT INTO USER_MENTION (mentionedUser,tweetid) VALUES(%s,%s)''',(mention['screen_name'],tweet_id,))
                            conn.commit()
                    if tweet['in_reply_to_status_id'] != null:
                        cursor.execute(''' SELECT * FROM REPLY WHERE userId = %s and tweetid = %s''',(tweet['user']['id'],tweet['in_reply_to_status_id'],))
                        rows = cursor.fetchcall()
                        if len(rows) == 0:
                            cursor.execute(''' INSERT INTO REPLY (userId,tweetid) VALUES(%s,%s)''',(tweet['user']['id'],tweet['in_reply_to_status_id'],))
                            conn.commit()
cursor.close()
conn.close()
