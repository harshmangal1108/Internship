#from email.mime.text import MIMEText
#from email.mime.multipart import MIMEMultipart
#import smtplib,ssl,getpass
from pymongo import MongoClient
from shutil import copyfile
import pandas as pd
import config as cfg 
import datetime
import csv
import schedule
import string
import yagmail
import xlsxwriter
import os

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

# ---Count in Query & Range---
def docs_count_interval_day(start_date_time,end_date_time,collection_name,query): #search_date="current_date"
    get_count_date=db[collection_name].count_documents(query)
    #print(query)
    #print("Count -->",get_count_date)
    return get_count_date

# ---Find Results(Aggregate)---
def aggregate_fucntion(start_date,end_date,group_by):
    records=db[cfg.collection_name].aggregate([
        #{"$match":{"created_date":{"$gte":start_date,"$lt":end_date}}},
        {"$match":{}},
        {"$group":{"_id":group_by,"Count":{"$sum":1}}}
    ])
    return list(records)

### Task:
"""
created date from config.. filed name
validate config field ex.. agar xyz hai to run
Match:--
group_by E/N field ,aggregate will call only it will be on...

"""







# ---Creating Data for Excel ---
reports_array=[]
def build_excel_data(From,To,name,query,count,sheet):
    report={
        "From":str(From),
        "To":str(To),
        "Name":name,
        "Query":query,
        "Count":count,
        "Sheet":sheet
    }
    reports_array.append(report)


# ---Checks and Converstions---
def from_main():
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
                    query1={cfgval["field_name"]:{'$gte':start_date,'$lt':end_date}}
                    query2=cfgval["filter"]
                    query=query1.copy()
                    query.update(query2)
                    end_date=datetime.datetime.strptime(end_date_str,'%Y-%m-%d %H:%M:%S')
                    docs_in_collection_range_day = docs_count_interval_day(start_date,end_date,collection_name,query)
                    ##Col name
                    #col_name=cfgval["group_by"].upper()
                    print("---",aggregate_fucntion(start_date,end_date,cfgval["group_by"]))
                    build_excel_data(start_date,end_date,cfgval["name"],query,docs_in_collection_range_day,cfgval["new_sheet_name"])

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
                    query1={cfgval["field_name"]:{'$gte':start_date,'$lt':end_date}}
                    query2=cfgval["filter"]
                    query=query1.copy()
                    query.update(query2)
                    docs_in_collection_range_day = docs_count_interval_day(start_date,end_date,collection_name,query)
                    #col_name=cfgval["group_by"].upper()
                    print("---",aggregate_fucntion(start_date,end_date,cfgval["group_by"]))
                    build_excel_data(start_date,end_date,cfgval["name"],query,docs_in_collection_range_day,cfgval["new_sheet_name"])

# ---Calling main function---
from_main()

# ---Creating and Spliting Excel---
df=pd.DataFrame(reports_array,columns=["From",'To','Name','Query','Count',"Sheet"])
#print(df)
df.to_excel("./Common Report.xlsx",sheet_name=cfg.new_sheet_name,index=False,engine='openpyxl')
file="./Common Report.xlsx"
df1=pd.read_excel(file)
extenxion=os.path.splitext(file)[1]
path=os.getcwd()
final_file=os.path.join(path,"Final Report"+""+extenxion)
#print()
column_pick="Sheet"
columns=list(set(df1[column_pick].values))
# ---Spliting Sheet---
def split_sheet(columns):
    copyfile(file,final_file)
    for _ in columns:
        writer=pd.ExcelWriter(final_file,engine="openpyxl")
        for sheet_name in columns:
            new_df=df.loc[df[column_pick]== sheet_name]
            new_df.to_excel(writer,sheet_name,index=False)
        writer.save()
split_sheet(columns)



# ---Sending Mail---
def mail_sender():
    sender = cfg.sender
    yag=yagmail.SMTP(sender,password=cfg.password)
    yag.login()
    yag.send(to=cfg.reciever,
         subject="Spliting Sheet",
         attachments=final_file,
         contents="Spliting Data Sheet Name wise is done.The approach and libraries are that only which we discussed"
        )
    
#mail_sender()

# ---Scheduling Task---
#schedule.every(15).seconds.do(mail_sender)
#while True:
##   schedule.run_pending()
 #   time.sleep(1)
