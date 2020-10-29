from pymongo import MongoClient
import pymongo
import config as cfg
import pprint
import datetime
import string
import pandas as pd
import json



client=MongoClient()
db=client[cfg.dbname]
print(db.list_collection_names())
group_by={
            "function_name":"$function_name",
            "client_id":"$client_id"
        }

def find_function():
    user=db[cfg.collection_name].aggregate([
        #{"$match":{"created_date":{"$gte":datetime.datetime.today()-datetime.timedelta(2),"$lt":datetime.datetime.today()}}},
        {"$group":{"_id":group_by,"Total Values":{"$sum":1}}}
    ])
    return list(user)
groups_list=[]
groups_values=[]
for val in find_function():
    groups_list.append(val['_id'])
    groups_values.append(val['Total Values'])
print(groups_list)
print(groups_values)
newlist=list(zip(groups_list,groups_values))
print(pd.DataFrame(newlist))
#print(find_function())
#print(pd.DataFrame(list(find_function().items()))) 
