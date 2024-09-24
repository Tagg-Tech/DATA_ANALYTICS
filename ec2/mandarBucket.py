import boto3
from datetime import datetime
s3_resource = boto3.resource("s3")
bucket = s3_resource.Bucket("tagtech-raw")



