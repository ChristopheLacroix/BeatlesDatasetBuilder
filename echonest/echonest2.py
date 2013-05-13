#!/usr/bin/env python
from pyechonest import config, song
from StringIO import StringIO
from subprocess import Popen, PIPE
import csv
import datetime
import time
import os
import json

API_KEY = "Q6GYW0YMKAJPLNBS2"
CONSUMER_KEY = "87a9a40b10958cf9cb0c4802ae5a3d09"
SHARED_SECRET = "pH2Aahv/R0yX6GpDLjo0RA"

config.ECHO_NEST_API_KEY=API_KEY

CMD="""curl "http://developer.echonest.com/api/v4/track/profile?api_key=Q6GYW0YMKAJPLNBS2&format=json&id={song_id}&bucket=audio_summary" """

song_map = {
    "back in the u.s.s.r.": "back in the u.s.s.r",
    "why don't we do it in the road?": "why don't we do it in the road",
    }

songs = {}
with open('tracks.txt') as f:
    for row in f:
        r = row.strip('\n').split(" >>> ")
        title = song_map.get(r[0], r[0])
        song_id = r[1]
        songs[title] = song_id

master_list = []
with open('../master-list.txt') as f:
    for row in f:
        master_list.append(row.strip('\n'))
master_list = sorted(master_list)

columns = ['title', 'echo_id', 'energy', 'tempo', 'speechiness', 'key', 'duration', 'liveness', 'mode', 'time_signature', 'loudness', 'danceability']

with open('echonest2.csv','w') as f:
    writer = csv.DictWriter(f, columns, delimiter=',', quotechar='`', quoting=csv.QUOTE_ALL)
    writer.writerow({x:x for x in columns})

    for title in master_list:
        print title

        title_key = title.lower()
        song_id = songs[title_key]
        cmd = CMD.format(song_id=song_id)

        status = None
        while status is None:
            p = Popen(
                cmd,
                shell=True,
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE)
            o = p.stdout.read()
            j = json.load(StringIO(o))

            status = j['response']['status']['message']
            if status != "Success":
                print " ", status
                print "  >> sleeping"
                time.sleep(60)
                status = None

        audio_summary = j['response']['track']['audio_summary']
        audio_summary["title"] = title
        audio_summary["echo_id"] = song_id
        del audio_summary["analysis_url"]

        writer.writerow(audio_summary)


# {u'response': {u'status': {u'code': 0, u'message': u'Success', u'version': u'4.2'}, u'track': {u'status': u'complete', u'song_id': u'SOHMFJC12C0DDC0226', u'audio_md5': u'5108dd3d41be891e2094265fe3eb9ea2', u'artist': u'The Beatles', u'samplerate': 44100, u'title': u"A Hard Day's Night", u'analyzer_version': u'3.1.3', u'artist_id': u'AR6XZ861187FB4CECD', u'bitrate': 320, u'id': u'TRJGMEA13E355D1955', u'audio_summary': {u'key': 7, u'analysis_url': u'http://echonest-analysis.s3.amazonaws.com/TR/TRJGMEA13E355D1955/3/full.json?AWSAccessKeyId=AKIAJRDFEY23UEVW42BQ&Expires=1366702169&Signature=e4Gt/7c9NwpU35ntwVCJ7f/mww0%3D', u'energy': 0.8429308827636494, u'liveness': 0.10310184530412887, u'tempo': 138.508, u'speechiness': 0.03957764490152532, u'mode': 1, u'time_signature': 4, u'duration': 154.17424, u'loudness': -7.207, u'danceability': 0.5885207880131782}, u'md5': u'b386abeb1d84585023ee10233b091bbc'}}}
