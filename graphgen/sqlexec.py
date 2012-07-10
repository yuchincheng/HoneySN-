import sqlite3

connection = sqlite3.connect("backup.db")
#connection.create()
   
cursor = connection.cursor()
cursor.execute("""
                CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, timestamp TEXT, host TEXT, source_addr TEXT, request TEXT, module INTEGER, filename TEXT, response TEXT)""")
connection.commit()

hp_conn = sqlite3.connect("../pool/db/glastopf.db")
c = hp_conn.cursor() 
#c.execute("""DELETE FROM events WHERE id=4868 """)

c.execute("""Select * from events where module="rfi" """)

for row in c:
    print row[0]
    cursor.execute("""INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    connection.commit()
c.close()
