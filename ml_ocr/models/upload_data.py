import os
import boto3
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://Novneet:jayhanuman1@cluster0.oxi79.mongodb.net/test?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.DIGIMACHINE


def upload_to_database(filename, upload_type=None):
    data = db['creds'].find_one()
    s3_bucket = 'digitalmachineocr'
    s3 = boto3.resource(
        service_name='s3',
        region_name='ap-south-1',
        aws_access_key_id=data['aws_access_key_id'],
        aws_secret_access_key=data['aws_secret_access_key']
    )
    file_content = open(os.path.join('./tmp', filename), 'rb')
    s3.Bucket(s3_bucket).put_object(Key=filename, Body=file_content)
    object = s3.Bucket(s3_bucket).Object(filename)
    # object.Acl().put(ACL='public-read')
    return filename
