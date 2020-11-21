# TODO: Unit Testing
uri = "mongodb://localhost:27017"
dbname = 'newdb'
is_active = 0
new_sheet_name = "Main"
is_groupby = 0
group_by = "function_name"
collection_name = 'statscollection'
collection_name_alias = "Stats"
sender = "harsh.mangal03acc@gmail.com"
reciever = ["harsh_student@citabu.ac.in"]
password = "harsh@1108google"
flag = 1
configuration_count_required_fields = ["name", "is_groupby", "is_active", "field_name", "new_sheet_name", "collection_name",
                                       "interval_date", "interval_time", "group_by", "filter"]
debug_mode = 0
configuration_count = {
    "stats_for_1": {
        "name": "Stats with filter",
        "uri": uri,
        "dbname": dbname,
        #"is_groupby": 1,
        "is_active": 1,
        "field_name": "created_date",
        "new_sheet_name": "My Sheet",
        "collection_name": 'statscollection',
        "interval_date": '2020-08-25',  # format- 'DD/MM/YY HH:MM:SS'
        "interval_time": '00:00:00',
        "interval_mode": "day",  # day,seconds,minutes by default = day
        "group_by": {
            "function_name": "$function_name",
            "status_code": "$status_code"
        },
        'filter': {
            'client_id': 'MNRNJVXE',
            'function_name': {'$eq': 'authorize'},
            'user_id': {'$ne': None},

        }
    },

    "stats_for_2": {
        "name": "Stats with filter",
        "uri": uri,
        "dbname": dbname,
        "is_groupby": 1,
        "is_active": 1,
        "field_name": "created_date",
        "new_sheet_name": "My Group",
        "collection_name": 'codinglang',
        "interval_date": '2020-08-28',
        "interval_time": '00:00:00',             # format- 'DD/MM/YY HH:MM:SS'
        "interval_mode": "day",  # day,seconds,minutes by default = day
        "group_by": {
            "client_id": "$client_id",
            "status_code": "$status_code"
        },
        'filter': {
            'client_id': 'MNRNJVXE',
            # 'function_name':{'$ne':'authorize'},
            # 'user_id':{'$ne':None},
        }
    },
    "stats_for_3": {
        "name": "Function Name Filter",
        "uri": uri,
        "dbname": dbname,
        "is_active": is_active,
        "is_groupby": is_groupby,
        "field_name": "created_date",
        "new_sheet_name": "Sheet 1",
        "collection_name": 'codinglang',
        "interval_mode": "day",  # day,seconds,minutes by default = day
        #interval_duration=1 ##
        "interval_date": '2020-10-06',
        "interval_time": '00:00:00',                 # format- 'DD/MM/YY HH:MM:SS'
        "group_by": {
            "client_id": "$client_id",
            "status_code": "$status_code"
        },
        'filter': {
            'name': 'Pascal'
            # 'client_id':'MNRNJVXE',
            # 'function_name':{'$eq':'authorize'},
            # 'user_id':{'$ne':None},
        }
    },

    "stats_for_4": {
        "name": "Stats for Date Range",
        "uri": uri,
        "dbname": dbname,
        "is_active": is_active,
        "is_groupby": is_groupby,
        "field_name": "created_date",
        "new_sheet_name": new_sheet_name,
        "collection_name": 'codinglang',
        "interval_mode": "day",  # day,seconds,minutes by default = day
        #interval_duration=1 ##
        "interval_date": '2020-08-25',
        "interval_time": '00:00:00',                 # format- 'DD/MM/YY HH:MM:SS
        "group_by": {
            "client_id": "$client_id",
            "status_code": "$status_code"
        },
        'filter': {
            # 'client_id':'MNRNJVXE',
            # 'function_name':{'$eq':'authorize'},
            # 'user_id':{'$ne':True},
        }
    }

}

# for k,v in configuration_count.items():
#     print()
#     if 'new_sheet_name' not in v:
#         print("no")
#     else:
#         print("Present")
