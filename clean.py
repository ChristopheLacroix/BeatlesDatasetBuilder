#!/usr/bin/env python
import csv
import os
import shutil

key_map = ["c","c#","d","d#","e","f","f#","g","g#","a","a#","b"]
mode_map = ["minor","major"]
songwriter_map = {
    "Lennon,": "Lennon",
    "McCartney, with Lennon": "McCartney",
    "Lennon, with McCartney": "Lennon",
    "(Traditional) arr. Lennon, McCartney, Harrison, Starkey": "Lennon, McCartney, Harrison and Starkey",
    "Lennon, with Ono and Harrison": "Lennon",
    "Harrison, with Lennon": "Harrison",
    "Lennon, with McCartney and Starkey": "Lennon",
    }

rows = []
with open('metadata.csv') as f:
    reader = csv.DictReader(f, delimiter=',', quotechar='`')
    columns = reader.fieldnames
    for row in reader:
        rows.append(row)

shutil.copy('metadata.csv', 'metadata.csv.tmp')

try:
    with open('metadata.csv','w') as f:
        writer = csv.DictWriter(f, columns, delimiter=',', quotechar='`', quoting=csv.QUOTE_ALL)
        writer.writerow({x:x for x in columns})

        for row in rows:
            row["key"] = key_map[int(row["key"])]
            row["mode"] = mode_map[int(row["mode"])]
            row["songwriter"] = songwriter_map.get(row["songwriter"]) or row["songwriter"]

            writer.writerow(row)
except:
    shutil.move('metadata.csv.tmp', 'metadata.csv')
else:
    os.remove('metadata.csv.tmp')

