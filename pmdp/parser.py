# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from operator import itemgetter

import os
import io
import boto3

from collections import Counter

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

class LogFileParser:
    __metaclass__  = ABCMeta

    @abstractmethod
    def parse(self): pass

class StringParser(LogFileParser):
    def __init__(self, llp, st):
        self.llp = llp
        self.st  = st

    def parse(self):
        llp = self.llp
        summary = Counter()
        for line in self.st.strip().split("\n"):
            summary[llp.parse_line(line)] += 1
        return summary

class S3Parser(LogFileParser):
    def __init__(self, llp, bucket, key):
        self.llp = llp
        self.bucket = bucket
        self.key = key

    def parse(self):
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=self.bucket, Key=self.key)
        sp = StringParser(self.llp, response['Body'].read())
        return sp.parse()

class FileParser(LogFileParser):
    def __init__(self, llp, fn):
        self.llp = llp
        self.fn  = fn

    def parse(self):
        llp = self.llp
        summary = Counter()
        with io.open(self.fn, 'r') as f:
            for line in f:
                summary[llp.parse_line(line)] += 1
        return summary

class DirectoryParser(LogFileParser):
    def __init__(self, llp, dr):
        self.llp = llp
        self.dr  = dr

    def parse(self):
        llp = self.llp
        summary = Counter()
        for f in os.listdir(self.dr):
            fn = os.path.join(self.dr, f)
            if os.path.isfile(fn):
                fp = FileParser(llp, fn)
                summary += fp.parse()
        return summary
