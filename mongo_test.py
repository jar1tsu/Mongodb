from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["sneaker_market_db"]

print(db.command("ping"))
print("collections:", db.list_collection_names())

