import boto3
import zipfile


def extract_and_unzip_from_s3(*args, **kwargs):
    
    # Read object from S3 using boto3
    
    # Extract files from zip file
    print()
    
    #Write them to a custom s3 bucket