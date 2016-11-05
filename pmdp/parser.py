# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from operator import itemgetter

class LogLineParser:
    __metaclass__  = ABCMeta

    @abstractmethod
    def parse_line(self, line): pass

class DatePathLogLineParser(LogLineParser):
    def parse_line(self, line):
        try:
            dt, path = itemgetter(0,12)(line.split(' '))
            dt = dt[:10] # Just the ymd
            path = path.split('/')[-1] # Ignore the host
            return (dt, path)
        except Exception as e:
            print('Failed to handle line', line, e)
            return ('','')
