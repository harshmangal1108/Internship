import openpyxl
import pandas as pd

vals=[1,2,3,4]
vals1=[0,0,0,0]
dfl=[]
writer=pd.ExcelWriter("./income.xlsx",engine="xlsxwriter")
for i in range(len(vals)):

    report={
    "value":[vals[i]],
    "vals 1":[vals1[i]]}
    df=pd.DataFrame(report)
    dfl.append(df)
    income_Sheets={"sheet{}".format(i+1):dfl[i]}
    print(income_Sheets)
    for sh in income_Sheets.keys():
        income_Sheets[sh].to_excel(writer,sheet_name=sh,index=False)










        
        
writer = pd.ExcelWriter('./income.xlsx', engine='xlsxwriter')

income1 = pd.DataFrame({'Names': ['Stephen', 'Camilla', 'Tom'],
                   'Salary':[100000, 70000, 60000]})

income2 = pd.DataFrame({'Names': ['Pete', 'April', 'Marty'],
                   'Salary':[120000, 110000, 50000]})

income3 = pd.DataFrame({'Names': ['Victor', 'Victoria', 'Jennifer'],
                   'Salary':[75000, 90000, 40000]})

income_sheets = {'Group1': income1, 'Group2': income2, 'Group3': income3}
print(income_sheets)


for sheet_name in income_sheets.keys():
    income_sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)

writer.save()
        