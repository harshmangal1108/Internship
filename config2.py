uri = "mongodb://localhost:27017"
dbname = 'newdb'
configuration_count = {
    "stats_for_1":{ 
        "uri" : uri,
        "dbname" : dbname,
        "collection_name":'statscollection',
        "collection_name_alias":"Stats",
        "interval_mode":"day", #day,seconds,minutes by default = day
        #interval_duration=1 ##
        "interval_date":'2020-08-25',
        "interval_time":'00:00:00',                 # format- 'DD/MM/YY HH:MM:SS'
        'sender':"harsh.mangal03acc@gmail.com",
        'reciever':"harsh_student@citabu.ac.in",
        'password':"password_here",
                #filters="public_ip"
           #filters_value="'127.0.0.1"
              #"ajit.kumar@digitalindia.gov.in"
        'filter':{
                 'client_id':'MNRNJVXE',
                 'function_name':{'$eq':'authorize'},
                 'user_id':{'$ne':None},

                    }
         },

    "stats_for_2":{ 
        "uri" : uri,
        "dbname" : dbname,
        "collection_name":'statscollection',
        "collection_name_alias":"Stats",
        "interval_mode":"day", #day,seconds,minutes by default = day
        #interval_duration=1 ##
        "interval_date":'2020-08-25',
        "interval_time":'00:00:00',                 # format- 'DD/MM/YY HH:MM:SS'
        'sender':"harsh.mangal03acc@gmail.com",
        'reciever':"harsh_student@citabu.ac.in",
        'password':"password_here",
                #filters="public_ip"
           #filters_value="'127.0.0.1"
              #"ajit.kumar@digitalindia.gov.in"
        'filter':{
                 'client_id':'MNRNJVXE',
                 'function_name':{'$ne':'authorize'},
                 'user_id':{'$ne':None},

                    }
         }

}
print(configuration_count)

collection_name='statscollection'
collection_name_alias="Stats"
interval_mode="day" #day,seconds,minutes by default = day
#interval_duration=1 ##
interval_date='2020-08-25'
interval_time='00:00:00'                 # format- 'DD/MM/YY HH:MM:SS'
sender="harsh.mangal03acc@gmail.com"
reciever="harsh_student@citabu.ac.in"
password="password_here"
#filters="public_ip"
#filters_value="'127.0.0.1"
#"ajit.kumar@digitalindia.gov.in"
filter={
    'client_id':'MNRNJVXE',
    'function_name':{'$eq':'authorize'},
    'user_id':{'$ne':None},

}

