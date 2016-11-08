# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from operator import itemgetter

# TODO: Parse ip, user agent

class LogLineParser:
    __metaclass__  = ABCMeta

    @abstractmethod
    def parse_line(self, line): pass

class DatePathLogLineParser(LogLineParser):
    def parse_line(self, line):
        dt, path = itemgetter(0,12)(line.split(' '))
        dt = dt[:10] # Just the ymd
        path = path.split('/')[-1] # Ignore the host
        return (dt, path)

