from pprint import pprint

from pymongo import MongoClient, GEOSPHERE
import json
from bson.objectid import ObjectId

# client = MongitaClientDisk()
try:
  client = MongoClient("mongodb+srv://greg:gregory123@cluster0.agji2kq.mongodb.net/?appName=Cluster0")
  
# return a friendly error if a URI error is thrown 
except pymongo.errors.ConfigurationError:
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)



db = client.geospatial_demo
places = db.places
places.drop()

with open("geo_locations.json") as f:
    data = json.load(f)
    places.insert_many(data)

places.create_index([("location", GEOSPHERE)])
print("Inserted and indexed locations.")
