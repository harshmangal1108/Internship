import pandas as pd
import os
from openpyxl import load_workbook
import xlsxwriter
from shutil import copyfile

file = "/home/harsh/Internship/SampleData.xlsx"


df= pd.read_excel(file)

colpick="Region"
cols=list(set(df[colpick].values))
extension=os.path.splitext(file)[1]
path=os.path.dirname(file)
newfile=os.path.join(path,"Report"+""+extension)
print(newfile)

#print(path)
#print(cols)
def send_to_sheet(cols):
    copyfile(file,newfile)
    for j in cols:
        writer=pd.ExcelWriter(newfile,engine="openpyxl")
        for my_name in cols:
            mydf=df.loc[df[colpick]==my_name]
            mydf.to_excel(writer,sheet_name=my_name,index=False)
        writer.save()

send_to_sheet(cols)