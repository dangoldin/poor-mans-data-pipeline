# -*- coding: utf-8 -*-

import unittest

import json
import os

from pmdp.parse_elb_log_lambda import lambda_handler
from pmdp.parser.line_parser import DatePathLogLineParser

class TestLambdaFunction(unittest.TestCase):
    # Valid end to end
    def test_valid_lambda_parse(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        with open(os.path.join(dir_path, 'test-s3-put.json'), 'r') as f:
            d = json.loads(f.read())
            out = lambda_handler(d, None)
            self.assertTrue(out['success'])

class TestDatePathLogLineParser(unittest.TestCase):
    # Valid line
    def test_valid_line_parse(self):
        line = """2016-10-22T22:35:17.425648Z poor-mans-data-pipeline 1.2.3.4:5 - -1 -1 -1 503 0 0 0 "GET http://poor-mans-data-pipeline.us-east-1.elb.amazonaws.com:80/PATH123 HTTP/1.1" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36" - -"""
        lp = DatePathLogLineParser()
        results = lp.parse_line(line)
        self.assertEquals('2016-10-22', results[0])
        self.assertEquals('PATH123', results[1])

    # Should throw exception
    def test_invalid_line_parse(self):
        line = "BAD LINE"
        lp = DatePathLogLineParser()
        try:
            results = lp.parse_line(line)
            self.fail("Should have thrown an exception")
        except Exception, e:
            pass

if __name__ == '__main__':
    unittest.main()
