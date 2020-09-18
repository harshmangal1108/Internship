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
import csv
import yagmail

### 
### Creating Connection
client=MongoClient(cfg.uri)
### Check available databases
print(client.list_database_names())

db_name=cfg.dbname                 ### FROM CONFIG FILE 
db=client[db_name]    
print(db.list_collection_names())
collection_name=cfg.collection_name ### FROM CONFIG FILE
## Doing our tasks
### *********** to count all records
def docs_count():
    funcn1=db[collection_name].count_documents({})
    return "Total Documents in {} On {} is: {} ".format(collection_name,datetime.datetime.today(),funcn1)
docs_in_collection=str(docs_count())
#print(docs_in_collection)
get_interval_mode = cfg.interval_mode  ### FROM CONFIG FILE
#get_interval_duration = cfg.interval_duration ### FROM CONFIG FILE
where=cfg.filters
what=cfg.filters_value
def docs_count_interval_day(start_date_time,end_date_time): #search_date="current_date"
   
    get_count_date=db[collection_name].count_documents(
        {
            'step':'2',where:what
        }
    )
    print(get_count_date)
    return "Total Documents in {} From {} To {} is: {}".format(collection_name,start_date,end_date,get_count_date)
    

### -----Checks and Converstions----

if get_interval_mode == 'day':
    if not cfg.interval_date or not cfg.interval_date.strip():
        previous_date=datetime.date.today()-datetime.timedelta(days=1)
        start_date_str=str(previous_date)+" "+"00:00:00"
        start_date=datetime.datetime.strptime(start_date_str,'%Y-%m-%d %H:%M:%S')
        print(start_date)
        end_date_str=str(datetime.date.today())+" "+"00:00:00"
        print(end_date_str)
        print("@@@@@@@@")
        end_date=datetime.datetime.strptime(end_date_str,'%Y-%m-%d %H:%M:%S')
        docs_in_collection_range_day = docs_count_interval_day(start_date,end_date)
        #print(docs_in_collection_range_day)
    else :
        start_date_time_str=cfg.interval_time

        #recieved_date=datetime.datetime.strptime(cfg.interval_date,'%Y-%m-%d %H:%M:%S')
        if not cfg.interval_time:
            start_date_time_str="00:00:00" 
            print("hello")           
        #docs_in_collection_range_day = docs_count_interval_day(start_date,end_date)
        #if not cfg.interval_time or not cfg.interval_time.strip():
        start_date_str=cfg.interval_date+" "+start_date_time_str
        start_date=datetime.datetime.strptime(start_date_str,'%Y-%m-%d %H:%M:%S')
        end_date_str_1=start_date.date()+datetime.timedelta(days=1)
        end_date_str=str(end_date_str_1)+" "+start_date_time_str
        end_date=datetime.datetime.strptime(end_date_str,'%Y-%m-%d %H:%M:%S')
        print(start_date)
        print(end_date)
        docs_in_collection_range_day = docs_count_interval_day(start_date,end_date)

        

        #print(docs_in_collection_range_dy)

with open("output.txt","w+") as f:
    f.write(docs_in_collection)
    f.write('\n')
    f.write(docs_in_collection_range_day)
    f.close()



def docs_count_interval_hour():
    pass

def mail_sender():
    sender = cfg.sender
    yag=yagmail.SMTP(sender)
    yag.login()
    yag.send(to=["harsh_student@citabu.ac.in"],
         subject="Testing Yagmail",
         attachments="/home/harsh/oauth_access_log_py_backend_job/output.txt",
         contents="This is data report"
        )
    
#mail_sender()

### scheduling task
            #-------
#schedule.every(15).seconds.do(mail_sender)
#while True:
##   schedule.run_pending()
 #   time.sleep(1)