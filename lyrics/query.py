#!/usr/bin/env python
import os
import csv
import re
from collections import defaultdict

song_words = {}
root = "lyrics"
for album in os.listdir(root):
    album_path = os.path.join(root, album)
    for song in os.listdir(album_path):
        if not song.endswith(".txt"):
            continue
        song_name = song[:-4]
        song_words[song_name] = defaultdict(int)
        song_path = os.path.join(album_path, song)
        with open(song_path) as f:
            for line in f:
                line = line.strip("\n")
                line = line.replace("--", " -- ")
                for word in line.split(" "):
                    word = word.replace("[","")
                    word = word.replace("]","")
                    word = word.replace("(","")
                    word = word.replace(")","")
                    word = word.replace(".","")
                    word = word.replace(",","")
                    word = word.replace("!","")
                    word = word.replace("?","")
                    word = word.replace('"',"")
                    word = word.replace(' ',"")
                    word = word.strip("'")
                    word = word.lower()

                    if word.count("-") > 2:
                        continue
                    elif word.count("-") == 2:
                        word.replace("-","")

                    if re.sub(r"[-]*", "", word) == "":
                        continue
                    if re.sub(r"[ah]*", "", word) == "":
                        continue
                    if re.sub(r"[oh]*", "", word) == "":
                        continue
                    if re.sub(r"[m]*", "", word) == "":
                        continue
                    if not re.search(r"[a-z0-9]", word):
                        continue
                    if word == "":
                        continue

                    song_words[song_name][word] += 1

# words_set = set()
# for song, words in song_words.iteritems():
#     for word in words.keys():
#         words_set.add(word)

# print "\n".join(words_set)

# quit()

columns = ["title","word_count", "unique_word_count", "longest_word"]

with open("lyrics.csv","w") as f:
    writer = csv.DictWriter(f, columns, delimiter=',', quotechar='`', quoting=csv.QUOTE_ALL)
    writer.writerow({x:x for x in columns})

    for song, words in song_words.iteritems():
        longest_word = None
        for word in words.keys():
            if longest_word is None or len(word) > len(longest_word):
                longest_word = word

        row = {
            "title": song,
            "word_count": sum(words.values()),
            "unique_word_count": len(words),
            "longest_word": longest_word,
            }

        writer.writerow(row)

# for album, words in album_words.iteritems():
#     print album.ljust(40), len(words)

# print "\n".join(["%s: %s" % (k,v) for k,v in sorted(words.items(), key=lambda x: -len(x[0]))])
