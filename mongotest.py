
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://effybizai:AhM2SPj8dKfLId89@cluster0.yfq6agh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Access the effy-ai-tagging database
db = client.get_database('effy-ai-tagging')

# Access the base_table collection
base_table = db.get_collection('base_table')

# Query the collection to retrieve the keywords field
result = base_table.find_one({}, {'uid': "5"})

if result:
    keywords = result.get('keywords', [])
    print(keywords)
else:
    print("No data found for keywords field in base_table.")
