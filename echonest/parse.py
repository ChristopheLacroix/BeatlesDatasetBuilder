#!/usr/bin/env python
import json
from StringIO import StringIO
import re

def get_file_key(f):
    file_key = f
    file_key = re.sub(r'^\d+\s', '', file_key)
    file_key = re.sub(r'\.mp3$', '', file_key)
    file_key = re.sub(r'\(\d\)$', '', file_key)
    file_key = re.sub(r' \[[^\]]*]$', '', file_key)
    file_key = file_key.lower()
    return file_key

lines = []
with open('upload-dump.txt') as f:
    for line in f:
        lines.append(json.load(StringIO(line.strip("\n"))))

with open('tracks.txt','w') as f:
    for line in lines:
        track = line['response']['track']
        s = "%s >>> %s" % (get_file_key(track['title']), track['id'])
        print s
        f.write(s+"\n")
