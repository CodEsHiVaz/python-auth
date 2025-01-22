from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

client = MongoClient(DATABASE_URL)
db = client.apiDb 
user_collection = db["user"]

