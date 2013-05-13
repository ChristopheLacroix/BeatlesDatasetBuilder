#!/usr/bin/env python
import mechanize
import csv
from bs4 import BeautifulSoup
import time
import os
import sys

br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_refresh(False)
br.addheaders = [('User-agent', 'Firefox')]

titles = []
with open('metadata.csv') as f:
    reader = csv.DictReader(f, delimiter=',', quotechar='`')
    for row in reader:
        titles.append(row["title"])

url="http://www.liwc.net/tryonline.php"
columns = ['title','self-references','social words','positive emotions','negative emotions','overall cognitive words','articles','big words']

with open('lyrics-info.csv','w') as f:    
    writer = csv.DictWriter(f, columns, delimiter=',', quotechar='`', quoting=csv.QUOTE_ALL)
    writer.writerow({x:x for x in columns})

    for i, title in enumerate(titles):
        # if i < 68:
        #     continue

        # print title, i
        # if title.lower() == "baby you're a rich man":
        #     quit()
        # continue

        print title.ljust(40),
        sys.stdout.flush()

        if title.lower() in ["revolution 9", "flying"]:
            print "SKIPPING"
            continue

        filename = None
        for x in os.listdir("/home/cedric/Downloads/beatles/lyrics"):
            if x.lower().replace(".txt","") == title.lower():
                filename = x

        with open("/home/cedric/Downloads/beatles/lyrics/"+filename) as l:
            lyrics = l.read()

        r = br.open(url)
        br.select_form("questionForm")
        br.set_all_readonly(False)
        br["Sex"] = ["NoDetails"]
        br["TextToLIWC"] = lyrics
        r = br.submit()
        html = r.read()

        soup = BeautifulSoup(html)
        row = {
            "title": title,
            'self-references': soup.findAll(text="Self-references (I, me, my)")[0].findNext("td").string,
            'social words': soup.findAll(text="Social words")[0].findNext("td").string,
            'positive emotions': soup.findAll(text="Positive emotions")[0].findNext("td").string,
            'negative emotions': soup.findAll(text="Negative emotions")[0].findNext("td").string,
            'overall cognitive words': soup.findAll(text="Overall cognitive words")[0].findNext("td").string,
            'articles': soup.findAll(text="Articles (a, an, the)")[0].findNext("td").string,
            'big words': soup.findAll(text="Big words (> 6 letters)")[0].findNext("td").string,
            }

        w = []
        for k,x in row.iteritems():
            if k != "title":
                w.append(str(x).ljust(8))
        print "".join(w)

        writer.writerow(row)
        time.sleep(1)
