#!/usr/bin/env python
from pyechonest import config, song
import csv
import datetime
import time
import os

API_KEY = "Q6GYW0YMKAJPLNBS2"
CONSUMER_KEY = "87a9a40b10958cf9cb0c4802ae5a3d09"
SHARED_SECRET = "pH2Aahv/R0yX6GpDLjo0RA"

config.ECHO_NEST_API_KEY=API_KEY

cols_order = [
    "title",
    "artist_name",
    "artist_id",
    "liveness",
    "duration",
    "tempo",
    "key",
    "mode",
    ]
cols = {
    "title": 60,
    "artist_name": 15,
    "artist_id": 20,
    "liveness": 15,
    "duration": 15,
    "tempo": 15,
    "key": 5,
    "mode": 5,
    }

master_list = []
with open('../master-list.txt') as f:
    for row in f:
        master_list.append(row.strip('\n'))
master_list = sorted(master_list)

missing = []
with open('missing.txt') as f:
    for row in f:
        missing.append(row.strip('\n'))
missing = sorted(missing)

song_titles = missing

columns = ['title', 'energy', 'tempo', 'speechiness', 'key', 'duration', 'liveness', 'mode', 'time_signature', 'loudness', 'danceability']

calls = []
done = 0

with open('echonest2.csv','w') as f:
    writer = csv.DictWriter(f, columns, delimiter=',', quotechar='`', quoting=csv.QUOTE_ALL)
    writer.writerow({x:x for x in columns})

    for title in song_titles:
        print "%s / %s complete" % (done, len(song_titles))
        done += 1

        one_min = datetime.datetime.now() - datetime.timedelta(minutes=1, seconds=5)
        num_calls = len(filter(lambda x: x > one_min, calls))
        if num_calls == 19:
            print "SLEEPING", datetime.datetime.now().strftime("%I:%M:%S")
            time.sleep(60)

        os.system("clear")
        print "%s" % title
        print

        songs = song.search(artist="the beatles",title=title,buckets=['id:7digital', 'tracks'])
        calls.append(datetime.datetime.now())

        def print_song(s, i):
            data = {
                "title": s.title,
                "artist_name": s.artist_name,
                "artist_id": s.artist_id,
                }
            data = dict(data.items() + s.audio_summary.items())

            row = ""
            for c in cols_order:
                d = data[c]
                if c == "duration":
                    d = "%s:%02d" % (int(d)/60, int(d) % 60)
                if c == "liveness":
                    d = str(d)[:10]
                row += str(d)[:cols[c]-1].ljust(cols[c]) if cols[c] else str(d)

            print "%s%s" % (str(i).ljust(3), row)

        def sorter(s):
            return s.audio_summary["liveness"]

        i = 0
        choices = {}
        for s in sorted(songs, key=sorter):
            if s.artist_id != "AR6XZ861187FB4CECD":
                continue
            i += 1

            if i == 1:
                row = ""
                for c in cols_order:
                    row += c.ljust(cols[c]) if cols[c] else c
                print "   %s" % row

            print_song(s, i)
            choices[i] = s

        print
        choice = raw_input("yes? ")
        while int(choice) not in choices:
            choice = raw_input("yes? ")

        info = choices[int(choice)]

        print
        print_song(info, choice)

        info.audio_summary["title"] = title
        del info.audio_summary["analysis_url"]
        del info.audio_summary["audio_md5"]

        writer.writerow(info.audio_summary)

        print
        raw_input("Enter to continue...")


# rows = get_rows()
# new_rows = []
# with open('info/songs-list.txt') as f:
#     for song in f:
#         title = song.strip("\n")
#         row = rows[title]
#         new_rows.append((row["Title"], row["Album"], row["Year"]))

# for x in sorted(new_rows, key=lambda x: (x[1], x[0])):
#     print x[0].ljust(60), x[1].ljust(40), x[2]

# quit()

# info_titles = set([row["Title"] for row in get_rows_filtered()])
# song_titles = set([l.strip("\n") for l in open('info/songs-list.txt')])

# print "INFO - SONGS"
# for x in sorted(list(info_titles - song_titles)):
#     print x
# print
# print "SONGS - INFO"
# for x in sorted(list(song_titles - info_titles)):
#     print x
# print
