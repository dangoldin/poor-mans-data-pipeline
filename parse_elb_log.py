#!/usr/bin/python

import os
import sys
import io
import csv
from operator import itemgetter
from collections import Counter

# TODOs: Parse ip, user agent

def parse_line(line):
    dt, path = itemgetter(0,12)(line.split(' '))
    dt = dt[:10] # Just the ymd
    path = path.split('/')[-1] # Ignore the host
    return (dt, path)

def process_file(fn):
    summary = Counter()

    with io.open(fn, 'r') as f:
        for line in f:
            summary[parse_line(line)] += 1

    return summary

def process_directory(d):
    summary = Counter()

    for f in os.listdir(d):
        fn = os.path.join(d, f)
        if os.path.isfile(fn):
            summary += process_file(fn)

    return summary

def write_to_csv(fn, headers, data):
    with open(fn, 'w') as f:
        w = csv.writer(f)
        w.writerow(headers + ['cnt',])
        w.writerows([i + (cnt,) for i, cnt in data.iteritems()])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Specify a file or directory'
        sys.exit(1)

    fn = sys.argv[1]

    if os.path.isdir(fn):
        out = process_directory(fn)
    else:
        out = process_file(fn)

    print out

    out_fn = 'out.csv'
    if len(sys.argv) == 3:
        out_fn = sys.argv[2]

    write_to_csv(out_fn, ['date', 'path'], out)
