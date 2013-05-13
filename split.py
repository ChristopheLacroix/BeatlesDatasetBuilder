#!/usr/bin/env python
import csv

# columns = ['title','year','album','songwriter','lead_vocals','chart_position_uk','chart_position_us']
columns = ['title','self_references','social_words','positive_emotions','negative_emotions','cognitive_words','articles','big_words']

with open('metadata.master.csv') as fr:
    # with open('wiki.csv','w') as fw:
    with open('liwc.csv','w') as fw:
        reader = csv.DictReader(fr, delimiter=',', quotechar='`')
        writer = csv.DictWriter(fw, columns, delimiter=',', quotechar='`', quoting=csv.QUOTE_ALL)
        writer.writerow({x:x for x in columns})
        for row in reader:
            newrow = {}
            for column in columns:
                newrow[column] = row[column]
            writer.writerow(newrow)
