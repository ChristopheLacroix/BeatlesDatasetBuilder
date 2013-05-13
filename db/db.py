#!/usr/bin/env python
import csv
import os
import shutil
from MySQLdb import connect

rows = []
with open('../metadata.csv') as f:
    reader = csv.reader(f, delimiter=',', quotechar='`')
    for i, row in enumerate(reader):
        if i == 0:
            columns = row
        else:
            rows.append(row)

con = None
try:
    con = connect(
        host='localhost',
        user='root',
        db='honr3310')

    cur = con.cursor()
    cur.execute("drop table if exists Song;")
    cur.execute("""
        create table Song (
            `id` int not null auto_increment primary key,
            `title` varchar(255),
            `year` int,
            `album` varchar(255),
            `songwriter` varchar(255),
            `lead_vocals` varchar(255),
            `chart_position_uk` int,
            `chart_position_us` int,
            `echo_id` varchar(255),
            `energy` float(11, 10),
            `tempo` float(6, 3),
            `speechiness` float(11, 10),
            `key` varchar(2),
            `duration` float(8, 5),
            `liveness` float(11, 10),
            `mode` varchar(5),
            `time_signature` int,
            `loudness` float(5, 3),
            `danceability` float(11, 10),
            `self_references` float(4, 2),
            `social_words` float(4, 2),
            `positive_emotions` float(4, 2),
            `negative_emotions` float(4, 2),
            `cognitive_words` float(4, 2),
            `articles` float(4, 2),
            `big_words` varchar(255),
            `word_count` int,
            `unique_word_count` int,
            `longest_word` varchar(255)
        );
    """)
    insert = []
    for row in rows:
        insert.append("  (%s)" % ','.join(['"%s"' % v if v!="" else "NULL" for v in row]))

    sql = "insert into Song(%s) values\n" % ','.join(['`%s`' % c for c in columns])
    sql+= ",\n".join(insert)
    cur.execute(sql)
    con.commit()

finally:
    if con:
        con.close()
