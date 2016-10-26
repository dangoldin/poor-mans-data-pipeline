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

print('Loading function')

s3 = boto3.client('s3')

def parse_line(line):
    try:
        dt, path = itemgetter(0,12)(line.split(' '))
        dt = dt[:10] # Just the ymd
        path = path.split('/')[-1] # Ignore the host
        return (dt, path)
    except Exception as e:
        print('Failed to handle line', line)
        return ('','')

def process_string(s):
    summary = Counter()
    for line in s.split("\n"):
        if line:
            summary[parse_line(line)] += 1
    return summary

def process_file(fn):
    summary = Counter()
    with io.open(fn, 'r') as f:
        for line in f:
            summary[parse_line(line)] += 1
    return summary

def process_directory(d):
    summary = Counter()
    for f in os.listdir(d):
        fn = os.path.join(d, f)
        if os.path.isfile(fn):
            summary += process_file(fn)
    return summary

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        print('Getting ',bucket,key)
        response = s3.get_object(Bucket=bucket, Key=key)
        summary = process_string(response['Body'].read())
        print(summary)
        return {'success': True}
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
