# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from operator import itemgetter

# TODO: Parse ip, user agent

class LogLineParser:
    """
    LogLineParser is the abstract class that handles parsing individal
    rows in the AWS ELB log file format.

    http://docs.aws.amazon.com/elasticloadbalancing/latest/classic/access-log-collection.html
    """

    __metaclass__  = ABCMeta

    @abstractmethod
    def parse_line(self, line): pass

class DatePathLogLineParser(LogLineParser):
    """
    DatePathLogLineParser is a simple log line parser that returns
    a date in ymd and the path.
    """

    def parse_ymd(self, dt_str):
        return dt_str[:10] # Just the ymd

    def parse_path(self, url):
        return url.split('/')[-1] # Skip the host name

    def parse_line(self, line):
        dt, url = itemgetter(0,12)(line.split(' '))
        dt = self.parse_ymd(dt)
        path = self.parse_path(url)
        return (dt, path)

class DatePathKeyLogLineParser(DatePathLogLineParser):
    """
    DatePathKeyLogLineParser is a log line parser that returns
    a date in ymd, the path, as well as the GET arg valus for
    the specified keys.
    """

    def __init__(self, keys):
        self.keys = keys

    def parse_path_and_keys(self, path):
        query_args = {}
        parts = path.split('?')
        if len(parts) == 2:
            for q in parts[1].split('&'):
                kv = q.split('=')
                if len(kv) == 2: # Only handle valid ones
                    query_args[kv[0]] = kv[1]

        return (parts[0], ) + tuple(query_args.get(k, '') for k in self.keys)

    def parse_line(self, line):
        dt, url = itemgetter(0,12)(line.split(' '))
        dt = super(DatePathKeyLogLineParser, self).parse_ymd(dt)
        path = super(DatePathKeyLogLineParser, self).parse_path(url)
        url_pieces = self.parse_path_and_keys(path)
        return (dt, ) + url_pieces
