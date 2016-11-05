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
from collections import Counter

from .parse_elb_log import process_string
from .writer import S3CSVFileWriter

print('Loading function')

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        print('Getting', bucket, key)
        response = s3.get_object(Bucket=bucket, Key=key)
        summary = process_string(response['Body'].read())
        print(summary)
        writer = S3CSVFileWriter(bucket, 'TEST')
        writer.write_summary(summary)
        return {'success': True}
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
