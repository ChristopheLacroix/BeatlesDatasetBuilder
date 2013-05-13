#!/usr/bin/env python
import csv
import time
import os
import sys
import re
import urllib2 as urllib

rows = []
url = None
title = None
while url is None or "theres-a-place" not in url:
    if url is None:
        url = "http://www.beatlesebooks.com/theres-a-place"
        title = "There's A Place"

    print title, "--", url

    r = urllib.urlopen(url)
    html = r.read()

    def get(label):
        r = re.search(
            r'<font size="2">.*?<strong>%s</strong>(.*?</span>.*?)</font>' % label,
            html,
            re.MULTILINE|re.DOTALL).group(1)
        letter = re.search(r'[A-G][0-9]?#?', r).group()
        mode = re.search(r'minor', r)
        if mode:
            mode = mode.group()
        else:
            mode = "major"
        return letter, mode

    letter, mode = get("Key")
    print " ", letter, mode
    rows.append({"title":title,"key":letter,"mode":mode})

    r = re.search(r'PREVIOUS.*?NEXT.*?<a href="([^"]*)">"([^"]*)"', html)
    url = r.group(1)
    title = r.group(2)


with open('beatlesbooks.csv','w') as f:
    writer = csv.DictWriter(f, ["title","key","mode"], delimiter=',', quotechar='`', quoting=csv.QUOTE_ALL)
    writer.writerow({"title":"title", "key":"key", "mode":"mode"})

    for row in rows:
        writer.writerow(row)
