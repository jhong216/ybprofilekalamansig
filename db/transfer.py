import sqlite3
from datetime import datetime

old=sqlite3.connect('./db/SNA.db')
cur=old.cursor()
cur.execute("Select fullname,precint,purok,barangay,bcm,hhno,status,birthday,occupation,hhtype from profile")
orw=cur.fetchall()

new=sqlite3.connect('./db/data.sqlite')
curn=new.cursor()
for i in orw:
    try:
        curn.execute("""INSERT INTO PROFILE(FULLNAME,PRECINT,SITIO,BARANGAY,CODE,OCCUPATION,TYPE)
                    VALUES(?,?,?,?,?,?,?)
                    """,(i[0],i[1],i[2],i[3],i[5],i[8],i[9]))
        print(i[0])
    except Exception as e:
        new.rollback()
        print(f'Error  - - -{e} {i[0]}')
new.commit()
