import os
import boto3
from pymongo import MongoClient


# db = client.DIGIMACHINE


# def upload_to_database(filename, upload_type=None):
#     data = db['creds'].find_one()
#     s3_bucket = 'panrange'
#     s3 = boto3.resource(
#         service_name='s3',
#         region_name='ap-south-1',
#         aws_access_key_id=data['aws_access_key_id'],
#         aws_secret_access_key=data['aws_secret_access_key']
#     )
#     file_content = open(os.path.join('./tmp', filename), 'rb')
#     s3.Bucket(s3_bucket).put_object(Key=filename, Body=file_content)
#     object = s3.Bucket(s3_bucket).Object(filename)
#     # object.Acl().put(ACL='public-read')
#     return filename


def get_db():
    client = MongoClient("mongodb://novacept:qhu5IVPqCjS3IQCI@ac-658ugvq-shard-00-00.wkfg1lx.mongodb.net:27017,"
                         "ac-658ugvq-shard-00-01.wkfg1lx.mongodb.net:27017,"
                         "ac-658ugvq-shard-00-02.wkfg1lx.mongodb.net:27017/?ssl=true&replicaSet=atlas-hg0dc7"
                         "-shard-0&authSource=admin&retryWrites=true&w=majority")

    # Create the database for our example (we will use the same database throughout the tutorial
    db = client.DigiMachine
    return db
