import urllib.parse
from pymongo import MongoClient
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

USERNAME = urllib.parse.quote_plus(config.get('default', 'username'))
PASSWORD = urllib.parse.quote_plus(config.get('default', 'password'))
DB_NAME = config.get('default', 'db_name')

# Correctly formatted MongoDB URI
MONGO_URL = f"mongodb+srv://{USERNAME}:{PASSWORD}@telemate.mkqh5.mongodb.net/{DB_NAME}?retryWrites=true&w=majority&appName=TeleMate"

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URL)
db = mongo_client[DB_NAME]

# Collections
users_collection = db["users"]               # Stores user details
chats_collection = db["chats"]               # Stores chat history
files_collection = db["files"]               # Stores image/file metadata
web_searches_collection = db["web_searches"] # Stores web search queries
reminders_collection = db["reminders"]       # Stores reminders
todos_collection = db["todos"]               # Stores to-do tasks