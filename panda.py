
import pymongo
import config2 as cfg
from pymongo import MongoClient
from pandas import ExcelWriter
import pandas as pd
import datetime
import yagmail
client=MongoClient()
db=client.newdb
print(db.list_collection_names())

get_count_date=db['statscollection'].count_documents(
            {
               'created_date':{'$gte':datetime.datetime(2020,8,21,0,0,0),'$lt':datetime.datetime(2020,9,11,00,00,00)} 
            }
        )

print(get_count_date)

report={
    'From':['{}'.format(datetime.datetime(2020,8,21,0,0,0))],
    'To'  : ['{}'.format(datetime.datetime(2020,9,11,00,00,00))],
    'Count': [get_count_date]
}

df=pd.DataFrame(report,columns=['From','To','Count'])
#print(df)
df.to_excel("output.xlsx",sheet_name='Sheet_name_1',index=False, engine='xlsxwriter')  
print("hi")
print(type(cfg.reciever))

def mail_sender():
    sender = cfg.sender
    yag=yagmail.SMTP(sender)
    yag.login()
    yag.send(to=cfg.reciever,
         subject="Testing Yagmail",
         attachments="/home/harsh/output.xlsx",
         contents="This is data report"
        )
mail_sender()