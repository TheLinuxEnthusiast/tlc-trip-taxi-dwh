
import boto3
from botocore.exceptions import ClientError
import logging
import sys
import os
import subprocess
import configparser

#home_="/home/workspace/airflow/dags"

config = configparser.ConfigParser()
config.read("dags/aws-master.cfg")
    
AWS_ACCESS_KEY = config['MASTER']['AWS_ACCESS_KEY']
AWS_SECRET_KEY = config['MASTER']['AWS_SECRET_KEY']


def create_bucket(bucket_name, 
                  ACCESS_KEY,
                  SECRET_KEY,
                  region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    
    Source: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3', 
                                     aws_access_key_id=ACCESS_KEY,
                                     aws_secret_access_key=SECRET_KEY)
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', 
                                     region_name=region,
                                     aws_access_key_id=ACCESS_KEY,
                                     aws_secret_access_key=SECRET_KEY)
            #location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_file(file_name, 
                bucket, 
                ACCESS_KEY,
                SECRET_KEY,
                object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    
    Source: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3',
                             aws_access_key_id=ACCESS_KEY,
                             aws_secret_access_key=SECRET_KEY)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
    


if __name__ == "__main__":
    
    arguments = sys.argv[1:]
    #print(arguments)
    if len(arguments) == 1:
        s3_local_bucket = arguments[0]
    else:
        print("Only one argument needed")
        quit()
    
    ## Install pip dependencies
    if os.path.exists("pip_dependencies.sh"):
        subprocess.call(['/bin/bash', './pip_dependencies.sh'])
    else:
        print("pip shell script is missing")
        quit()
        
    ## Create S3 Bucket with bucket name passed by user
    create_bucket(s3_local_bucket, 
                  AWS_ACCESS_KEY, 
                  AWS_SECRET_KEY, 
                  region="us-east-1")
    
    
    ## Upload Taxi base data to taxi_base/taxi_base_lookup.csv
    upload_file("datasets/taxi_base_lookup.csv", 
                s3_local_bucket, 
                AWS_ACCESS_KEY, 
                AWS_SECRET_KEY, 
                object_name="taxi_base/taxi_base_lookup.csv")
    