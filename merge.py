#!/usr/bin/env python
import csv
import sys

#
# load csv files
#

columns = ['title']

def extract(path):
    global columns
    d = {}
    with open(path) as f:
        reader = csv.DictReader(f, delimiter=',', quotechar='`')
        for fieldname in reader.fieldnames[1:]:
            if fieldname not in columns:
                columns.append(fieldname)
        for row in reader:
            title = row['title'].lower()
            del row['title']
            d[title] = row
    return d

wiki = extract('wiki/wiki.csv')
echo = extract('echonest/echonest2.csv')
liwc = extract('liwc/liwc.csv')
lyrics = extract('lyrics/lyrics.csv')

#
# load master list
#

master_list = []
with open('master-list.txt') as f:
    for row in f:
        master_list.append(row.strip('\n'))
master_list = sorted(master_list)

#
# check for missing files
#

bad = False
for title in master_list:
    title = title.lower()
    missing = []
    if title not in wiki:
        missing.append("wiki")
    if title not in echo:
        missing.append("echo")
    if title not in liwc:
        missing.append("liwc")
    if title not in lyrics:
        missing.append("lyrics")
    if missing:
        print "%s%s" % (title.ljust(60), ",".join(missing))
        bad = True
if bad:
    print
    print "^^ please fix missing files"
    sys.exit(1)

#
# merge
#

with open('metadata.csv','w') as f:
    writer = csv.DictWriter(f, columns, delimiter=',', quotechar='`', quoting=csv.QUOTE_ALL)
    writer.writerow({x:x for x in columns})

    for title in master_list:
        title_key = title.lower()

        wiki_row = wiki[title_key]
        echo_row = echo[title_key]
        liwc_row = liwc[title_key]
        lyrics_row = lyrics[title_key]

        row = dict(wiki_row.items() + echo_row.items() + liwc_row.items() + lyrics_row.items())
        row["title"] = title

        writer.writerow(row)

