#!/usr/bin/env python
import os
from subprocess import Popen, PIPE
import csv
import re

columns = ['analysis_sample_rate','audio_md5','danceability','duration','end_of_fade_in','energy','idx_bars_confidence','idx_bars_start','idx_beats_confidence','idx_beats_start','idx_sections_confidence','idx_sections_start','idx_segments_confidence','idx_segments_loudness_max','idx_segments_loudness_max_time','idx_segments_loudness_start','idx_segments_pitches','idx_segments_start','idx_segments_timbre','idx_tatums_confidence','idx_tatums_start','key','key_confidence','loudness','mode','mode_confidence','start_of_fade_out','tempo','time_signature','time_signature_confidence','track_id']

out = "title,"+",".join(columns)+"\n"

root = "TheBeatlesHDF5"
for d in os.listdir(root):
    for s in os.listdir(os.path.join(root, d)):
        title = re.sub(r".*_-_", "", s)[:-3].replace("_"," ")
        print title

        cmd = 'h5ls -d "%s/analysis/songs"' % os.path.join(root, d, s)
        p = Popen(
            cmd,
            shell=True,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE)

        o = p.stdout.read()
        o = "".join([x.strip()[5:] for x in o.split("\n")[-4:-1]])[:-1]+"\n"
        o = o.replace(" ","")
        o = '"%s",%s' % (title, o)
        out += o

with open('msd.original.csv','w') as f:
    f.write(out)

