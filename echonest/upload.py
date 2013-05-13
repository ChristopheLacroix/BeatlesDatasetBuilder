#!/usr/bin/env python
from subprocess import Popen, PIPE
import os
import datetime
import re
import sys

CMD="""curl -F "api_key=Q6GYW0YMKAJPLNBS2" -F "filetype=mp3" -F "track=@{path}" "http://developer.echonest.com/api/v4/track/upload" """

#
# get all file paths
#

def get_file_key(f):
    file_key = f
    file_key = re.sub(r'^\d+\s', '', file_key)
    file_key = re.sub(r'\.mp3$', '', file_key)
    file_key = re.sub(r'\(\d\)$', '', file_key)
    file_key = re.sub(r' \[[^\]]*]$', '', file_key)
    file_key = file_key.lower()
    return file_key

files = {}
root = "/home/cedric/Downloads/beatles/"
for d in os.listdir(root):
    for s in os.listdir(os.path.join(root, d)):
        if os.path.isdir(os.path.join(root,d,s)):
            for x in os.listdir(os.path.join(root,d,s)):
                files[get_file_key(x)] = os.path.join(root,d,s,x)
        else:
            files[get_file_key(s)] = os.path.join(root,d,s)

#
# check against master list
#

master_list = []
with open('../master-list.txt') as f:
    for row in f:
        master_list.append(row.strip('\n'))
master_list = sorted(master_list)

bad = False
for title in master_list:
    title_key = title.lower()
    if title_key not in files:
        print title
        bad = True
if bad:
    print
    print "^^ please resolve missing files"
    print
    print "ALL FILES"
    print "\n".join(files.keys())
    sys.exit(1)

#
# check what has already been done
#

done = set()
with open('upload-done.txt') as f:
    for row in f:
        done.add(row.strip('\n'))

print "Already done:"
print "\n".join(done)
print

#
# create the todo queue
#

queue = []
for title in master_list:
    title_key = title.lower()
    if files[title_key] not in done:
        queue.append(files[title_key])

#
# execute the queue
#

with open('upload-done.txt','a') as done:
    with open('upload-dump.txt','a') as dump:
        for i, f in enumerate(sorted(queue)):
            print f.ljust(150), datetime.datetime.now().strftime("%I:%M:%S"), "(%s/%s)" % (i, len(queue))
            cmd = CMD.format(path=f)
            p = Popen(
                cmd,
                shell=True,
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE)
            o = p.stdout.read()
            if '"message": "Success"' not in o:
                print "stdout:"
                print o
                print "stderr:"
                print p.stderr.read()
                raise Exception("FAIL!")

            dump.write(o+"\n")
            done.write(f+"\n")

