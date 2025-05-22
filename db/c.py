import sqlite3


import xlwings as xw

db=sqlite3.connect('./db/data.sqlite')
cur=db.cursor()
# Specifying a sheet
ws = xw.Book("./db/cluster.xlsx").sheets['Sheet2']

# Selecting data from
# a single cell
v1 = ws.range("A:B").value

# for i in v1:
#     cur.execute("insert into cluster(precint,no) values(?,?)",(i[0],i[1]))
#     print(i)
# db.commit()
for i in  v1:
    if i[0]!='':
        print(i)
    else:
        break