#!/usr/bin/env python
import csv
import os

filemap = {}
lyrics = set()
for x in os.listdir("lyrics"):
    name = x.replace(".txt","").lower()
    lyrics.add(name)
    filemap[name] = os.path.join("lyrics",x)

titles = set()
with open("../master-list.txt") as f:
    for row in f:
        titles.add(row.lower().strip("\n"))

# for f in sorted(list(lyrics - titles)):
#     y = raw_input("%s? " % f)
#     if y.lower() != "n":
#         os.remove(filemap[f])

# quit()

print "LYRICS - TITLES"
print "\n".join(sorted(list(lyrics - titles)))
print
# print "TITLES"
# print "\n".join(sorted(list(titles)))

print "TITLES - LYRICS"
print "\n".join(sorted(list(titles - lyrics)))
print
# print "LYRICS"
# print "\n".join(sorted(list(lyrics)))
