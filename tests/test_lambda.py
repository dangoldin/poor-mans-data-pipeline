# -*- coding: utf-8 -*-

import unittest

import json

from pmdp.parse_elb_log_lambda import lambda_handler

class TestLambdaFunction(unittest.TestCase):

    def test_valid_lambda_parse(self):
        with open('test-s3-put.json', 'r') as f:
            d = json.loads(f.read())
            out = lambda_handler(d, None)
            self.assertTrue(out['success'])

if __name__ == '__main__':
    unittest.main()
