from pymongo_get_database import get_database
dbname = get_database()
collection_name = dbname["time_series_data"]
from dateutil import parser
import time
from bson import ObjectId
import datetime

# Fetch a document from the collection
doc = collection_name.find_one()
# Print the document
print(doc)


unix_timestamp = 1713548961
dt = datetime.datetime.fromtimestamp(unix_timestamp)
bson_datetime = ObjectId.from_datetime(dt)

print("Unix timestamp:", unix_timestamp)
print("BSON datetime:", bson_datetime)

bson_datetime_value = bson_datetime.generation_time

item_3 = {
    "time": bson_datetime_value,
    "item_name": "Bread",
    "quantity": 2,
    "ingredients": "all-purpose flour"
}

collection_name.insert_one(item_3)