# -*- coding: utf-8 -*-

import os
import sys

from pmdp.parser import DatePathLogLineParser, FileParser, DirectoryParser
from pmdp.writer import CSVFileWriter

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Specify a file or directory'
        sys.exit(1)

    fn = sys.argv[1]
    lp = DatePathLogLineParser()

    if os.path.isdir(fn):
        p = DirectoryParser(lp, fn)
    else:
        p = FileParser(lp, fn)
    out = p.parse()

    out_fn = 'out.csv'
    if len(sys.argv) == 3:
        out_fn = sys.argv[2]

    w = CSVFileWriter(out_fn)
    w.write_summary(out)
