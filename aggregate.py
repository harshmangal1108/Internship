from pymongo import MongoClient
import pymongo
import config as cfg
import pprint
import datetime
import string



client=MongoClient()
db=client[cfg.dbname]
print(db.list_collection_names())


def find_function():
    user=db[cfg.collection_name].aggregate([
        #{"$match":{"created_date":{"$gte":datetime.datetime.today()-datetime.timedelta(2),"$lt":datetime.datetime.today()}}},
        {"$group":{"_id":{"Funtion_wise":"$function_name"},"Total Values":{"$sum":1}}}
    ])
    return list(user)


pprint.pprint(find_function())
string="client_id"

print(string.upper())