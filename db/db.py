import sqlite3
def connection():
    db=sqlite3.connect('./db/data.sqlite')
    return db

def createtable():
    db=connection()
    cur=db.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS PROFILE(
                [ID] INTEGER PRIMARY KEY AUTOINCREMENT,
                [FULLNAME] TEXT NOT NULL UNIQUE,
                [PRECINT] TEXT NOT NULL,
                [SITIO] TEXT NOT NULL,
                [BARANGAY] TEXT NOT NULL,
                [GROUPING] TEXT NOT NULL,
                [CODE] TEXT NOT NULL)
                """)
    
    cur.execute("""
                CREATE TABLE IF NOT EXISTS PROFILETYPE(
                [ID] INTEGER PRIMARY KEY AUTOINCREMENT,
                [DESCRIPTION] TEXT NOT NULL UNIQUE,
                [PROJECT] TEXT NOT NULL,
                [TYPES] TEXT NOT NULL,
                [DATE] REAL)
                """)
    
    cur.execute("""
                CREATE TABLE IF NOT EXISTS COORDINATOR(
                [ID] INTEGER PRIMARY KEY AUTOINCREMENT,
                [NAME] TEXT NOT NULL UNIQUE,
                [TYPE] TEXT NOT NULL,
                [PUROK] TEXT NOT NULL,
                [BARANGGAY] TEXT NOT NULL)
                """)
    
    
    db.commit()


def voters():
    db=connection()
    cur=db.cursor()
    cur.execute("Select Voters")


def barangay():
    f=open("./db/barangay.txt","r",encoding="utf8")
    a=f.readlines()
    f.close
    return a

def coordinator_type():
    f=open("./db/type.txt","r",encoding="utf8")
    a=f.readlines()
    f.close
    return a
    
connection()
createtable()



