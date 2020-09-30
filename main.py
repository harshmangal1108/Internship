#from email.mime.text import MIMEText
#from email.mime.multipart import MIMEMultipart
#import smtplib,ssl,getpass
from pymongo import MongoClient
import datetime
import csv
import schedule
import time
import config2 as cfg 
import string
import pandas as pd
import yagmail
import xlsxwriter
# ---Creating Connection---
client=MongoClient(cfg.uri)
print(client.list_database_names()) # Check available databases
db_name=cfg.dbname                  # FROM CONFIG FILE 
db=client[db_name]    
print(db.list_collection_names())

# ---Count all Records---
total_documents_list=[]
def docs_count():
    for i in range(len(cfg.configuration_count)):
        total_documents=db[cfg.configuration_count["stats_for_{}".format(i+1)]["collection_name"]].count_documents({})
        total_documents_list.append(total_documents)
    #print(type(total_documents_list))
    return total_documents_list
print(docs_count())
#get_interval_mode = cfg.interval_mode  ### FROM CONFIG FILE
#get_interval_duration = cfg.interval_duration ### FROM CONFIG FILE

# ---Count in Query & Range---
def docs_count_interval_day(start_date_time,end_date_time,collection_name,query): #search_date="current_date"
    get_count_date=db[collection_name].count_documents(query)
    print(query)
    print("Count -->",get_count_date)
    return get_count_date

# --- Writing to Excel ---
def excel_sheet(From,To,name,query,count):
    report={
        "From":str(From),
        "To":str(To),
        "Name":name,
        "Query":query,
        "Count":count
    }
    df=pd.DataFrame(report,columns=["From",'To','Name','Query','Count'])
    df.to_excel("./report.xlsx",sheet_name=name,index=False,engine='xlsxwriter')

# ---Checks and Converstions---

for cfgkey,cfgval in cfg.configuration_count.items():
    collection_name=cfgval["collection_name"]
    if cfgval["is_active"]== 1:
        if cfgval["interval_mode"] == 'day':
            print(cfgkey)
            if not cfgval["interval_date"] or not cfgval["interval_date"].strip():
                previous_date=datetime.date.today()-datetime.timedelta(days=1)
                start_date_str=str(previous_date)+" "+"00:00:00"
                start_date=datetime.datetime.strptime(start_date_str,'%Y-%m-%d %H:%M:%S')
                #print(start_date)
                end_date_str=str(datetime.date.today())+" "+"00:00:00"
                #print(end_date_str)
                query1={'created_date':{'$gte':start_date,'$lt':end_date}}
                query2=cfgval["filter"]
                query=query1.copy()
                query.update(query2)
                end_date=datetime.datetime.strptime(end_date_str,'%Y-%m-%d %H:%M:%S')
                docs_in_collection_range_day = docs_count_interval_day(start_date,end_date,collection_name,query)
                excel_sheet(start_date,end_date,cfgval["name"],query,docs_in_collection_range_day)

                #print(docs_in_collection_range_day)
            else :
                start_date_time_str=cfgval["interval_time"]

                #recieved_date=datetime.datetime.strptime(cfg.interval_date,'%Y-%m-%d %H:%M:%S')
                if not cfgval["interval_time"]:
                    start_date_time_str="00:00:00" 
                    print("hello")           
                #docs_in_collection_range_day = docs_count_interval_day(start_date,end_date)
                #if not cfg.interval_time or not cfg.interval_time.strip():
                start_date_str=cfgval["interval_date"]+" "+start_date_time_str
                start_date=datetime.datetime.strptime(start_date_str,'%Y-%m-%d %H:%M:%S')
                end_date_str_1=start_date.date()+datetime.timedelta(days=1)
                end_date_str=str(end_date_str_1)+" "+start_date_time_str
                end_date=datetime.datetime.strptime(end_date_str,'%Y-%m-%d %H:%M:%S')
                #print(start_date)
                #print(end_date)
                query1={'created_date':{'$gte':start_date,'$lt':end_date}}
                query2=cfgval["filter"]
                query=query1.copy()
                query.update(query2)
                docs_in_collection_range_day = docs_count_interval_day(start_date,end_date,collection_name,query)
                excel_sheet(start_date,end_date,cfgval["name"],query,docs_in_collection_range_day)


def docs_count_interval_hour():
    pass

# --- Sending Mail ---

def mail_sender():
    sender = cfg.sender
    yag=yagmail.SMTP(sender,password=cfg.password)
    yag.login()
    yag.send(to=cfg.reciever,
         subject="Testing Yagmail",
         attachments="/home/harsh/oauth_access_log_py_backend_job/output.xlsx",
         contents="This is data report"
        )
    
#mail_sender()

# --- scheduling Task ---
#schedule.every(15).seconds.do(mail_sender)
#while True:
##   schedule.run_pending()
 #   time.sleep(1)
