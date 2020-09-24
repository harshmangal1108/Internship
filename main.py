from pymongo import MongoClient
#from email.mime.text import MIMEText
#from email.mime.multipart import MIMEMultipart
#import smtplib,ssl,getpass
import datetime
import csv
import schedule
import time
import config2 as cfg 
import string
import pandas as pd
import yagmail

### 
### Creating Connection
client=MongoClient(cfg.uri)
### Check available databases
print(client.list_database_names())

db_name=cfg.dbname             ### FROM CONFIG FILE 
db=client[db_name]    
print(db.list_collection_names())
#collection_name=cfg.configuration_count ### FROM CONFIG FILE
## Doing our tasks
### *********** to count all records
total_documents_list=[]

def docs_count():
    for i in range(len(cfg.configuration_count)):
        total_documents=db[cfg.configuration_count["stats_for_{}".format(i+1)]["collection_name"]].count_documents({})
        total_documents_list.append(total_documents)
    print(type(total_documents_list))
    return total_documents_list
print(docs_count())













#get_interval_mode = cfg.interval_mode  ### FROM CONFIG FILE
#get_interval_duration = cfg.interval_duration ### FROM CONFIG FILE
def docs_count_interval_day(start_date_time,end_date_time,collection_name,query): #search_date="current_date"
    get_count_date=db[collection_name].count_documents(query)
    print("From Here--",get_count_date)
    return get_count_date
  


### -----Checks and Converstions----
for cfgkey,cfgval in cfg.configuration_count.items():
    collection_name=cfgval["collection_name"]
    if cfgval["interval_mode"] == 'day':
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
        

        #print(docs_in_collection_range_dy)

"""with open("output.txt","w+") as f:
    f.write(docs_in_collection)
    f.write('\n')
    f.write(docs_in_collection_range_day)
    f.close()"""
### Putting all output into excel
print(docs_in_collection_range_day)
report={
    'From':['{}'.format(datetime.datetime(2020,8,21,0,0,0))],
    'To'  : ['{}'.format(datetime.datetime(2020,9,11,00,00,00))],
    'Count': [docs_in_collection_range_day]
    }

df=pd.DataFrame(report,columns=['From','To','Count'])
print(df)
df.to_excel("/home/harsh/oauth_access_log_py_backend_job/output.xlsx",sheet_name="Sheet_1",index=False,engine='xlsxwriter')


def docs_count_interval_hour():
    pass

def mail_sender():
    sender = cfg.sender
    yag=yagmail.SMTP(sender)
    yag.login()
    yag.send(to=["harsh_student@citabu.ac.in"],
         subject="Testing Yagmail",
         attachments="/home/harsh/oauth_access_log_py_backend_job/output.xlsx",
         contents="This is data report"
        )
    
#mail_sender()

### scheduling task
            #-------
#schedule.every(15).seconds.do(mail_sender)
#while True:
##   schedule.run_pending()
 #   time.sleep(1)
