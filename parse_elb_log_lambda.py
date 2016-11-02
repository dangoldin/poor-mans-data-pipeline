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

from parse_elb_log import process_string

print('Loading function')

s3 = boto3.client('s3')

def write_summary(bucket, key, summary):
    output = io.BytesIO()
    w = csv.writer(output)
    for k, v in summary.iteritems():
        w.writerow(k + (v,))
    s3.put_object(Bucket=bucket, Key=key, Body=output.getvalue())

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        print('Getting', bucket, key)
        response = s3.get_object(Bucket=bucket, Key=key)
        summary = process_string(response['Body'].read())
        print(summary)
        write_summary(bucket, 'TEST', summary)
        return {'success': True}
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
