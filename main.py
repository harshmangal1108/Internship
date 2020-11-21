from pymongo import MongoClient
from flask import Flask, Response, render_template, request, jsonify
from flask_restful import Resource, Api
from shutil import copyfile
import pandas as pd
import numpy as np
import datetime
import csv
import pprint
import string
import yagmail
import xlsxwriter
import os
from os import path
import json
import config as cfg
from bson import json_util, ObjectId


######################
# Creating Connection
######################
# client=MongoClient(cfg.uri)
# print(client)
# db_name=cfg.dbname
# db=client[db_name]

######################
# Global values
######################
total_documents_list = []
columns = []

file = "./Common Report.xlsx"
status = True
message = "Success"
validation_message = ""


######################
# Count all docs
######################
def docs_count():
    for i in range(len(cfg.configuration_count)):
        total_documents = db[
            cfg.configuration_count["stats_for_{}".format(
                i + 1)]["collection_name"]
        ].count_documents({})
        total_documents_list.append(total_documents)
    return total_documents_list


######################
##Count in Query & Range
######################
def docs_count_interval_day(
    cfgval, start_date_time, end_date_time, collection_name, query
):
    client = MongoClient(cfgval["uri"])
    db_name = cfgval["dbname"]
    db = client[db_name]
    get_count_date = db[collection_name].count_documents(query)
    return get_count_date


######################
# Find Results(Aggregate)
######################
def aggregate_fucntion(cfgval, start_date, end_date, query, group_by):
    client = MongoClient(cfgval["uri"])
    db_name = cfgval["dbname"]
    db = client[db_name]
    records = db[cfgval["collection_name"]].aggregate(
        [{"$match": query}, {"$group": {"_id": group_by, "Count": {"$sum": 1}}}]
    )
    return list(records)


# ---Convert aggaregate dictonary to dataframe
group_list = []
group_values = []
aggregate_report_row = {}


def aggregate_indataframe(
    From, To, name, query, group_by, sheet, result_aggregate_dictonary
):
    global aggregate_report_row
    for val in result_aggregate_dictonary:
        query1 = query
        query2 = {"Group_by": group_by}
        query = query1.copy()
        query.update(query2)
        aggregate_report_row = {
            "From": str(From),
            "To": str(To),
            "Name": name,
            "Query": query,
        }
        for gpkey, gpgval in group_by.items():
            aggregate_report_row[gpkey] = val["_id"][gpkey]

        aggregate_report_row["Count"] = val["Count"]
        aggregate_report_row["Sheet"] = sheet
        reports_array.append(aggregate_report_row)


######################
# Creating Data for Excel
######################
reports_array = []


def build_excel_data(From, To, name, query, count, sheet):
    global reports_array
    global aggregate_report_row
    aggregate_report_row = {
        "From": str(From),
        "To": str(To),
        "Name": name,
        "Query": query,
        "Count": count,
        "Sheet`": sheet,
    }
    reports_array.append(aggregate_report_row)

# Check Fields---


def check_fields(config_keys, config_values):
    global check_field_length
    global validation_message
    global status
    global fields
    # print(config_values.keys())
    try:
        if cfg.configuration_count_required_fields:
            fields = cfg.configuration_count_required_fields
            check_field_length = len(fields)
            check_list = []
            for field in fields:
                if field not in config_values.keys():
                    # check_flag=0
                    check_list.append(field)
            length_list = len(check_list)
            # print(check_list)
            if length_list > 0:
                status = False
                validation_message += config_keys + \
                    " : Fields '{}' is Not Present in Configuration File, ".format(
                        ",".join(check_list))
                return False
            return True

    except Exception as e:
        message = e


######################
##Checks and Converstions
######################
def from_main(con):
    global message
    global validation_message
    concount = len(con)
    if concount == 1:
        reports_array = []
    for cfgkey, cfgval in con.items():
        index = 0
        collection_name = cfgval["collection_name"]
        checked = check_fields(cfgkey, cfgval)
        if checked != True:
            # validation_message += validation_message
            continue
        if cfgval["is_active"] == 1:
            if cfgval["interval_mode"] == "day":
                if not cfgval["interval_date"] or not cfgval["interval_date"].strip():
                    previous_date = datetime.date.today() - datetime.timedelta(days=1)
                    start_date_str = str(previous_date) + "T" + "00:00:00.000Z"
                    start_date = datetime.datetime.strptime(
                        start_date_str, "%Y-%m-%dT%H:%M:%S"
                    )
                    end_date_str = str(datetime.date.today()
                                       ) + "T" + "00:00:00.000Z"
                    end_date = datetime.datetime.strptime(
                        end_date_str, "%Y-%m-%dT%H:%M:%S"
                    )
                    query1 = {
                        cfgval["field_name"]: {
                            "$gte": start_date, "$lt": end_date}
                    }
                    query2 = cfgval["filter"]
                    query = query1.copy()
                    query.update(query2)

                    if cfgval["is_groupby"] == 1:
                        result_aggregate_dictonary = aggregate_fucntion(
                            cfgval, start_date, end_date, query, cfgval["group_by"]
                        )
                        result_aggregate = aggregate_indataframe(
                            start_date,
                            end_date,
                            cfgval["name"],
                            query,
                            cfgval["group_by"],
                            cfgval["new_sheet_name"],
                            result_aggregate_dictonary,
                        )
                    else:
                        docs_in_collection_range_day = docs_count_interval_day(
                            cfgval, start_date, end_date, collection_name, query
                        )
                        build_excel_data(
                            start_date,
                            end_date,
                            cfgval["name"],
                            query,
                            docs_in_collection_range_day,
                            cfgval["new_sheet_name"],
                        )
                else:
                    start_date_time_str = cfgval["interval_time"]
                    if not cfgval["interval_time"]:
                        start_date_time_str = "00:00:00.000Z"
                    start_date_str = cfgval["interval_date"] + \
                        "T" + start_date_time_str
                    start_date = datetime.datetime.strptime(
                        start_date_str, "%Y-%m-%dT%H:%M:%S"
                    )
                    end_date_str_1 = start_date.date() + datetime.timedelta(days=1)
                    end_date_str = str(end_date_str_1) + \
                        "T" + start_date_time_str
                    end_date = datetime.datetime.strptime(
                        end_date_str, "%Y-%m-%dT%H:%M:%S"
                    )
                    query1 = {
                        cfgval["field_name"]: {
                            "$gte": start_date, "$lt": end_date}
                    }
                    query2 = cfgval["filter"]
                    query = query1.copy()
                    query.update(query2)
                    if cfgval["is_groupby"] == 1:
                        result_aggregate_dictonary = aggregate_fucntion(
                            cfgval, start_date, end_date, query, cfgval["group_by"]
                        )
                        result_aggregate = aggregate_indataframe(
                            start_date,
                            end_date,
                            cfgval["name"],
                            query,
                            cfgval["group_by"],
                            cfgval["new_sheet_name"],
                            result_aggregate_dictonary,
                        )
                    else:
                        docs_in_collection_range_day = docs_count_interval_day(
                            cfgval, start_date, end_date, collection_name, query
                        )
                        build_excel_data(
                            start_date,
                            end_date,
                            cfgval["name"],
                            query,
                            docs_in_collection_range_day,
                            cfgval["new_sheet_name"],
                        )
    if validation_message != "":
        message = validation_message

######################
# Creating and Spliting Excel
######################


def generate_data_to_excel():
    global status
    global message
    global aggregate_report_row
    try:
        if file.endswith(".xlsx"):
            df = pd.DataFrame(
                reports_array, columns=aggregate_report_row.keys())
            df.to_excel(
                file, sheet_name=cfg.new_sheet_name, index=False, engine="openpyxl"
            )
        else:
            status = False
            message = "Check extension of File it should be .xlsx"
        return df
    except Exception as e:
        status = False
        message = "Check extension of File it should be .xlsx"
        if cfg.debug_mode == 1:
            message = e


######################
# Spliting Sheet
######################
def split_sheet(df):
    global status
    global message
    df1 = pd.read_excel(file)
    extenxion = os.path.splitext(file)[1]
    path = os.getcwd()
    final_file = os.path.join(path, "Final Report" + "" + extenxion)
    column_pick = "Sheet"
    column_length = len(df1.columns)
    columns = []
    if column_length > 0:
        columns = list(set(df1[column_pick].values))
        copyfile(file, final_file)
        for _ in columns:
            writer = pd.ExcelWriter(final_file, engine="openpyxl")
            for sheet_name in columns:
                new_df = df.loc[df[column_pick] == sheet_name]
                new_df.to_excel(writer, sheet_name, index=False)
            writer.save()
    return final_file


######################
# Sending Mail
######################
def mail_sender(final_file, flag):
    global status
    global message
    try:
        if flag:
            sender = cfg.sender
            yag = yagmail.SMTP(sender, password=cfg.password)
            yag.login()
            yag.send(
                to=cfg.reciever,
                subject="Spliting Sheet",
                attachments=final_file,
                contents="Spliting Data Sheet Name wise is done.The approach and libraries are that only which we discussed",
            )
    except Exception as e:
        status = False
        message = "Mail server error or check your credentials"
        if cfg.debug_mode == 1:
            message = e


######################
# api function
######################
def run_main(con, flag):
    global status
    global message
    global reports_array
    try:
        path.exists(file)
        from_main(con)
        df = generate_data_to_excel()
        final_file = split_sheet(df)
        mail_sender(final_file, flag)
        output = reports_array
        reports_array = []
        aggregate_report_row = {}
        return {"status": status, "message": message, "records": output}
    except Exception as e:
        return {"status": status, "message": e}
