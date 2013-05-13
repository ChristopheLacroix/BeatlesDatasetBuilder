#!/usr/bin/env python
from bs4 import BeautifulSoup
import urllib2
import re
import sys

errors = []
with open('lyrics2.txt') as f:
    title = None
    lyrics = []
    for line in f:
        line = line.strip("\n")
        if not line:
            continue

        if title is None:
            title = line.replace(" ----------------------------------------",'')
            lyrics = []
            title = " ".join([y.capitalize() for y in title.split(" ")])
            print title,
            sys.stdout.flush()
        elif "----------------------------------------" in line:
            path = "lyrics/"+title+".txt"
            try:
                with open(path, 'w') as f:
                    print "> writing", path
                    f.write("\n".join(lyrics))
            except IOError:
                print "> ERROR"
                errors.append(title)
            title = line.replace(" ----------------------------------------",'')
            lyrics = []
            title = " ".join([y.capitalize() for y in title.split(" ")])
            print title,
            sys.stdout.flush()
        else:
            lyrics.append(line)

print
print "ERRORS"
print ",".join(errors)

quit()

# response = urllib2.urlopen("http://beatlesnumber9.com/lyrics.html")
# print response.info()
# html = response.read()

# print html.decode("iso-8859-1").encode("UTF-8")
# quit()

with open('lyrics.txt') as f:
    html = f.read()

soup = BeautifulSoup(html)

# print html

print
print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

for link in soup.find_all('a'):
    href = link.get('href')
    if href and href.startswith("#"):
        title = [x.encode("utf-8") for x in link.contents][0]
        print
        print title, "----------------------------------------"
        lyrics = re.search(r'name=%s.*?TOP' % href[1:], html, flags=re.DOTALL|re.MULTILINE).group()

        lyrics = re.sub(r'name=%s></a>' % href[1:], '', lyrics)
        lyrics = re.sub(r'<p>', '', lyrics)
        lyrics = re.sub(r'<br>', '', lyrics)
        lyrics = re.sub(r'\r', '', lyrics)
        lyrics = re.sub(r'<center><a href="#top">TOP', '', lyrics)
        lyrics = lyrics.decode("Windows-1252").encode("utf-8")

        # lyrics = lyrics.decode("iso-8859-1").encode("UTF-8")
        lyrics = "\n".join(filter(lambda x: x != '', lyrics.split("\n")[1:]))

        print lyrics
