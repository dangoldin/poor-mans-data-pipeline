# Poor Man's Data Pipeline
A minimal way to get a data pipeline up and running

## Motivation
Most data pipelines require heavy infrastructure and scale to get them running. The intent of Poor Man's Data Pipeline is to come up with something that's simple, cheap, yet robust enough to handle significant data volumes.

## How it works
The idea here is to leverage Amazon's Elastic Load Balancer configuration options to log every single request to an S3 bucket. This is paired with a Lambda function that takes the log data out of these S3 buckets and aggregates it for quick use.
