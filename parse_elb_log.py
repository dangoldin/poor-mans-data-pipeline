#!/usr/bin/python

import sys
import io
from operator import itemgetter

# TODOS: Parse ip, user agent

def process_file(fn):
    with io.open(fn, 'r') as f:
        for line in f:
            dt, path = itemgetter(0,12)(line.split(' '))
            dt = dt[:10] # Just the ymd
            path = path.split('/')[-1] # Ignore the host
            print dt, path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Specify a file'
        sys.exit(1)

    fn = sys.argv[1]

    process_file(fn)
