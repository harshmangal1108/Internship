uri = "mongodb://localhost:27017"
dbname = 'newdb'
is_active=0
configuration_count = {
    "stats_for_1":{ 
        "name":"Stats with filter",
        "uri" : uri,
        "dbname" : dbname,
        "is_active":0,
        "collection_name":'statscollection',
        "interval_mode":"day", #day,seconds,minutes by default = day
        #interval_duration=1 ##
        "interval_date":'2020-08-25',
        "interval_time":'00:00:00',                 # format- 'DD/MM/YY HH:MM:SS'
        'filter':{
                 'client_id':'MNRNJVXE',
                 'function_name':{'$eq':'authorize'},
                 'user_id':{'$ne':None},

                    }
         },

    "stats_for_2":{ 
        "uri" : uri,
        "dbname" : dbname,
        "is_active":is_active,
        "collection_name":'statscollection',
        "collection_name_alias":"Stats",
        "interval_mode":"day", #day,seconds,minutes by default = day
        #interval_duration=1 ##
        "interval_date":'2020-08-25',
        "interval_time":'00:00:00',                 # format- 'DD/MM/YY HH:MM:SS'
        'filter':{
                 'client_id':'MNRNJVXE',
                 'function_name':{'$ne':'authorize'},
                 'user_id':{'$ne':None},

                    }
         },
    "stats_for_3":{ 
        "name":"Function Name",
        "uri" : uri,
        "dbname" : dbname,
        "is_active":1,
        "collection_name":'collection',
        "interval_mode":"day", #day,seconds,minutes by default = day
        #interval_duration=1 ##
        "interval_date":'2020-08-25',
        "interval_time":'00:00:00',                 # format- 'DD/MM/YY HH:MM:SS'
        'filter':{
                 'client_id':'MNRNJVXE',
                 'function_name':{'$eq':'authorize'},
                 'user_id':{'$ne':None},

                    }
         },
    "stats_for_4":{ 
        "name":"Stats for Date Range",
        "uri" : uri,
        "dbname" : dbname,
        "is_active":1,
        "collection_name":'statscollection',
        "interval_mode":"day", #day,seconds,minutes by default = day
        #interval_duration=1 ##
        "interval_date":'2020-08-25',
        "interval_time":'00:00:00',                 # format- 'DD/MM/YY HH:MM:SS
        'filter':{
                 #'client_id':'MNRNJVXE',
                 #'function_name':{'$eq':'authorize'},
                 #'user_id':{'$ne':True},

                    }
         }

}
collection_name='statscollection'
collection_name_alias="Stats"
interval_mode="day" #day,seconds,minutes by default = day
#interval_duration=1 #
interval_date='2020-08-25'
interval_time='00:00:00'                 # format- 'DD/MM/YY HH:MM:SS'
sender="harsh.mangal03acc@gmail.com"
reciever=["harsh_student@citabu.ac.in","ajit.kumar@digitalindia.gov.in","ajitcse1215@gmail.com"]
password="harsh@1108google"
