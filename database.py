# database.py
from pymongo import MongoClient
from config import mongo_uri, db_name, collection_name

client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]
