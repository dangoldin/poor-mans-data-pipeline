# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import csv
import io
import boto3

class SummaryWriter:
    __metaclass__  = ABCMeta

    @abstractmethod
    def write_summary(self, summary): pass

class CSVFileWriter(SummaryWriter):
    def __init__(self, fn):
        self.fn = fn

    def write_summary(self, summary):
        with open(self.fn, 'w') as f:
            w = csv.writer(f)
            # TODO: Figure out header
            # w.writerow(headers + ['cnt',])
            w.writerows([i + (cnt,) for i, cnt in summary.iteritems()])

class S3CSVFileWriter(SummaryWriter):
    def __init__(self, bucket, key):
        self.bucket = bucket
        self.key = key
        self.s3 = boto3.client('s3')

    def write_summary(self, summary):
        output = io.BytesIO()
        w = csv.writer(output)
        for k, v in summary.iteritems():
            w.writerow(k + (v,))
        print 'Wrtiing to',self.bucket,self.key
        self.s3.put_object(Bucket=self.bucket, Key=self.key, Body=output.getvalue())
