#!/usr/bin/env python
import os
from subprocess import Popen, PIPE
import csv
import re

with open('msd.original.csv') as fr:
    with open('msd.csv','w') as fw:
        reader = csv.DictReader(fr, delimiter=',', quotechar='"')
        writer = csv.DictWriter(fw, reader.fieldnames, delimiter=',', quotechar='`', quoting=csv.QUOTE_ALL)
        writer.writerow({x:x for x in reader.fieldnames})
        for row in reader:
            writer.writerow(row)
