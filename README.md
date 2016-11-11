# Poor Man's Data Pipeline
A minimal way to get an extremely robust, scalable, and cheap data pipeline up and running.

## Motivation
Most data pipelines require a large infrastructure to get up and running. The intent of Poor Man's Data Pipeline is to use a variety of "serverless" components in order to build a data pipeline that has very few points of failure while still scaling to large volumes at low cost.

## How it works
The pipeline works by using Amazon's Elastic Load Balancer with access logs enabled. These logs are then stored on S3 and are parsed and aggregated via simple Lambda functions.

## Components
This project is still a work in progress but the components are listed below. A simple way to see how they're wired together is to take a look at the parse_elb_log_lambda.py file which is configured to be called by an AWS lambda function.
- Line parser: This is responsible for parsing each line of an S3 access log file. This is what you will need to change in order to support configure your logging levels.
- File parser: This just runs the line parser across each line of the log file. There are few options here for testing but generally you'll want to use the S3Parser class.
- Summary writer: This takes the result of the parse and exports it. At the moment I only have a simple writer back to S3 but one can build additional functionality to write it to a database or send the summary to another service.

## How to get it working
You will need to do two things.

1. Set up an Elastic Load Balancer and enable access logging. Note that you don't need to connect any instances to it since it will still be able to log every request. Note that responses to the ELB will have a 503 status code.
![alt text](https://github.com/dangoldin/poor-mans-data-pipeline/raw/master/img/pmdp-elb.png "PMDP ELB setup")

2. Set up an AWS Lambda function to parse the resulting access logs. The default code will do a simple count grouped by date and path and then upload them back to the original bucket. You can set up AWS Lambda by creating a zip archive and setting it up in the AWS console.

```
cd pmdp
zip -r lambda.zip *
```

![alt text](https://github.com/dangoldin/poor-mans-data-pipeline/raw/master/img/pmdp-lambda.png "PMDP Lambda setup")
