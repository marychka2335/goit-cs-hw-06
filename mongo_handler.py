from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

url = "mongodb://mongodb:27017"

client = MongoClient(url, server_api = ServerApi('1'))
db = client['message_database']
message_collection = db['messages']

#Only add new data to mongodb with unique date
def create_message(data):
    try:
        current_dateTime = datetime.now()
        data["date"] = data.get('date', current_dateTime)
        print(data)
        message_collection.insert_one(data)
    except Exception as e:
        print(e)