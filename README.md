# Poor Man's Data Pipeline
A minimal way to get a data pipeline up and running

## Motivation
Most data pipelines require heavy infrastructure and scale to get them running. The intent of Poor Man's Data Pipeline is to come up with something that's simple, cheap, yet robust enough to handle significant data volumes.

## How it works
The idea here is to leverage Amazon's Elastic Load Balancer configuration options to log every single request to an S3 bucket. This is paired with a Lambda function that takes the log data out of these S3 buckets and aggregates it for quick use.

## How to get it working
You will need to do two things.

1. Set up an Elastic Load Balancer and enable access logging. Note that you don't need to connect any instances to it since it will still be able to log every request. Note that responses to the ELB will have a 503 status code.
![alt text](https://github.com/dangoldin/poor-mans-data-pipeline/raw/master/src/img/pmdp-elb.png "PMDP ELB setup")

2. Set up an AWS Lambda function to parse the resulting access logs. The default code will do a simple count grouped by date and path and then upload them back to the original bucket. You can set up AWS Lambda by creating a zip archive and setting it up in the AWS console.

```
zip lambda.zip *py pmdp/*py
```

![alt text](https://github.com/dangoldin/poor-mans-data-pipeline/raw/master/src/img/pmdp-lambda.png "PMDP Lambda setup")
