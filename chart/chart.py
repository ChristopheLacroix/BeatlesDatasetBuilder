#!/usr/bin/env python
import csv
import os
import shutil
import numpy
from collections import defaultdict

X_AXIS = "year"
Y_AXIS = "danceability"

data = defaultdict(list)
with open('../metadata.csv') as f:
    reader = csv.DictReader(f, delimiter=',', quotechar='`')
    for row in reader:
        data[row[X_AXIS]].append(float(row[Y_AXIS]))

def reject_outliers(data, m=2):
    u = numpy.mean(data)
    s = numpy.std(data)
    return [e for e in data if (u - m * s < e < u + m * s)]

for x, y in sorted(data.iteritems()):
    fx = reject_outliers(y)
    print str(x).ljust(10), numpy.mean(y) if y else "nil"




# columns = [X_AXIS, Y_AXIS]
# outfile = "%s.%s.csv" % (X_AXIS, Y_AXIS)
# with open(outfile,'w') as f:
#     writer = csv.writer(f, delimiter=',', quotechar='`', quoting=csv.QUOTE_ALL)
#     writer.writerow(columns)
#     for row in sorted(data):
#         writer.writerow(row)
