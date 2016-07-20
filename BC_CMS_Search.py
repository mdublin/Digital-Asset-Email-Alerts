
#! /usr/bin/python
# -*- coding: utf-8 -*-

import feedparser

# import email alert 
from email_alert import send_alert

# db imports
from models import Base, Video
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///notifications.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# create video table object
#Video = models.Video()


# receiving user_tag text submitted by user via TagSearchForm on
# http://127.0.0.1:5000/protected



def mediaload():

    video_feed = "http://api.brightcove.com/services/library?command=search_videos&all=tag:smgv&all=tag:rio%202016&output=mrss&media_delivery=http&sort_by=CREATION_DATE:DESC&token={API READ TOKEN}"

    d = feedparser.parse(video_feed)

    # checking feed for any errors (i.e. "bozo" errors: https://pythonhosted.org/feedparser/bozo.html#advanced-bozo), bozo_exception will still exist in the parse response, but it's value would be 
    
    if 'bozo_exception' in d:
        print 'bozo_exception', d['bozo_exception']
        return d['bozo_exception']
    
    response_array = []

    # list returned of dicts for each video, this will be sent to, and
    # iterated through, videofeed.html endpoint with jinja2 control structures
    asset_return_list = []

    # -- For each item in the feed
    for index, post in enumerate(d.entries):
        #print index, post

        if index >= 1:
            break
        # Here we set up a dictionary in order to extract selected data from the
        # original brightcove "post" result
        item = {}

        item['name'] = post.title,
        item['description'] = post.description,
        item['url'] = u"%s" % post.link,
        # item['tags'] = post.media_keywords.split(",")
        item['videoID'] = post.bc_titleid,

        max_bitrate = 0
        vid_url = None
        #videos = post.media_content

        # trying to deal with this errory that only occurs occasionally for reasons yet not known:
        # feedparser.py", line 400, in __getattr__ raise AttributeError, "object has no attribute '%s'" % key AttributeError: object has no attribute 'media_content'

        try:
            videos = post.media_content
            
            # -- For each video in the item dict
            for video in videos:
            # -- If the video has a value for its bitrate
                if 'bitrate' in video:
                # -- Extract the value of this video's bitrate
                    bitrate_str = video['bitrate']
        # -- and convert it to an integer (by default it is a string in the XML)
                    curr_bitrate = int(bitrate_str)
            # -- If the bitrate of this video is greater than
            # -- the highest bitrate we've seen, mark this video as the one with
            # -- the highest birate.
                    if curr_bitrate > max_bitrate:
                        max_bitrate = curr_bitrate
                    vid_url = video['url']
        # -- This line simply prints out the maximum bitrate and current video URL for each iteration
        # print "{} url {}".format(max_bitrate, vid_url)
        # print "highest bitrate {} url {}".format(max_bitrate, vid_url)

        except AttributeError:
        #    print("post.media_content is throwing an AttributeError...probably for no reason. Keep refreshing the page or restart the server.")
            videos = "http://127.0.0.1:8000/"
            vid_url = videos        

        # get thumbnail image URL 
        try:
            thumbnails = post.media_thumbnail[0]
            thumbnail_url = thumbnails['url']
        except AttributeError:
            thumbnail_url = None
        
        #print thumbnails
        #thumbnail_url = None
        #max_height = 90
        
        #for thumbnail in thumbnails:
        #    if 'height' in thumbnail:
        #        height = thumbnail['height']
        #        if height == '90':
        #            thumbnail_url = thumbnail['url']

        tags = post.media_keywords

        item['tags'] = tags
        item['url'] = vid_url
        item['thumbnail'] = thumbnail_url

        videoID = item['videoID']
        # new line
        videoName = item['name']
        response_array.append(item)

        videoID = str(videoID)
        videoUrl = vid_url
        # videoName = str(videoName) #we have to convert videoName to a plain
        # old string instead of leaving it as unicode because the dudupe
        # function in our db script is "seeing" the video titles in our db
        for i in videoName:
            videoNameConverted = i  # Extracting the video title out of the tuple its in, so we can get string utf-8 encoded. So everwhere below this, we're replacing videoName with videoNameConverted
        # foo = type(i)
        # print "this is type check of tuple extract on line 70: %s" % foo
        videoDescription = item['description']
        
    #video_package = {}
    for asset_dict in response_array:
        video_package = {}
        extract_sourcefile_tupe = asset_dict['url']
        extract_thumbnail_tupe = asset_dict['thumbnail']
        extract_videoID_tupe = asset_dict['videoID']
        extract_name_tupe = asset_dict['name']
        extract_description_tupe = asset_dict['description']
        extract_tags_tupe = asset_dict['tags']

        video_package.update(
            {
                'videoID': extract_videoID_tupe[0],
                'name': extract_name_tupe[0],
                'description': extract_description_tupe[0],
                'tags': extract_tags_tupe,
                'url': extract_sourcefile_tupe,
                'thumbnail': extract_thumbnail_tupe
            }
        )
        
        asset_return_list.append(video_package)

    # list to dict 
    alert_video_package = asset_return_list[0]
    
    check_video_id = alert_video_package["videoID"]

    # check if videoID just pulled has already been included in email alert
    video = session.query(Video).filter_by(bc_id = check_video_id).first()
    if video:
        print "An alert for videoID: %s has already be sent" % (check_video_id)
    if not video:
        print "Sending alert...."
        # call email script with video asset package     
        send_alert(alert_video_package)
    
    return asset_return_list


if __name__ == "__main__":
    mediaload()


