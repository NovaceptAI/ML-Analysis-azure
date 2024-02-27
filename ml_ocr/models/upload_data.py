# import os
# import boto3
import pymongo

ENV = "qa"


def get_db():
    global client
    if ENV == "qa":
        client = pymongo.MongoClient("mongodb+srv://novacept:QdH3bIChIEMyDXBr@panrange-cluster.wkfg1lx.mongodb.net"
                                     "/?retryWrites "
                                     "=true&w=majority")
    elif ENV == "dev":
        client = pymongo.MongoClient("mongodb://localhost:27017")

    # Create the database for our example (we will use the same database throughout the tutorial
    db = client.DigiMachine
    return db
