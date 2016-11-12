# -*- coding: utf-8 -*-

from __future__ import print_function

import urllib

import datetime
import uuid

from parser.line_parser import DatePathLogLineParser
from parser.file_parser import S3Parser
from writer.s3_csv_writer import S3CSVFileWriter

print('Loading function')

def generate_filename():
    out_path = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    return out_path + '/' + str(uuid.uuid4())

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        # print('Getting', bucket, key)
        lp = DatePathLogLineParser()
        sp = S3Parser(lp, bucket, key)
        summary = sp.parse()
        print(summary)
        writer = S3CSVFileWriter(bucket, generate_filename())
        writer.write_summary(summary)
        return {'success': True}
    except Exception as e:
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
