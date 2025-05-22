import sqlite3
db=sqlite3.connect('./db/data.sqlite')
cur=db.cursor()
p=[
'0069A',
'0069B',
'0070A',
'0071A'

]

N=str(17)
for c in p:
        cur.execute("update voters set cluster='"+N+"' where precint='"+ c +"'")
        print(c)
        db.commit()

