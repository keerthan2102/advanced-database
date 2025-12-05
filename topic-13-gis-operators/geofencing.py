from pymongo import MongoClient

import pymongo
from bson.objectid import ObjectId

try:
  client = pymongo.MongoClient("mongodb+srv://greg:gregory123@cluster0.agji2kq.mongodb.net/?appName=Cluster0")
  
# return a friendly error if a URI error is thrown 
except pymongo.errors.ConfigurationError:
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)
  
db = client.geospatial_demo
zones = db.zones  # stores polygon boundaries

def in_zone(lat, lon):
    match = zones.find_one({
        "area": {
            "$geoIntersects": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                }
            }
        }
    })
    return match["zone"] if match else None

if __name__ == "__main__":
    zone_name = in_zone(40.76, -73.98)
    if zone_name:
        print(f"✔ Inside zone: {zone_name}")
    else:
        print("✘ Outside all zones")
