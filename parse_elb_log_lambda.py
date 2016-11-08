# -*- coding: utf-8 -*-

from __future__ import print_function

import json
import urllib
import boto3

import os
import sys
import io
import csv
import json
from operator import itemgetter
import datetime
import uuid

from pmdp.parser.line_parser import DatePathLogLineParser
from pmdp.parser.file_parser import S3Parser
from pmdp.writer.s3_csv_writer import S3CSVFileWriter

print('Loading function')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        print('Getting', bucket, key)
        lp = DatePathLogLineParser()
        sp = S3Parser(lp, bucket, key)
        summary = sp.parse()
        print(summary)
        out_path = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        writer = S3CSVFileWriter(bucket, out_path + '/' + str(uuid.uuid4()))
        writer.write_summary(summary)
        return {'success': True}
    except Exception as e:
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
