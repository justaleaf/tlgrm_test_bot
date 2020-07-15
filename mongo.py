from pymongo import MongoClient
import gridfs


client = MongoClient('localhost', 27017)
db = client.bot_data
collection = db.user_audio
fs = gridfs.GridFS(db)

