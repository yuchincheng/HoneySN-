import re
import sqlite3

#This code is for building up rfigraph.db from gastopf.db and sandbox.db

class LogSQLite():    
    def __init__(self):
        self.connection = sqlite3.connect("rfigraph.db")
        self.dbcreate()
    
    def dbclose(self):
        self.connection.close()
    
    def dbcreate(self):
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS 
                events(id INTEGER PRIMARY KEY, 
                analysis_date TEXT, 
                attacker_addr TEXT,
                rfi_file_url TEXT,
                rfi_file_md5 TEXT, 
                irc_addr INTEGER,  
                irc_channel TEXT)
                """)
        self.connection.commit()
        #self.cursor.close()
        
        
    def insert(self, itemall):
	#`print itemall
        self.cursor = self.connection.cursor()
        for graphinfo in itemall: 
	    graphinfo.insert(0,None)
            if(len(graphinfo)== 5):
                graphinfo.insert(5, None)
                graphinfo.insert(6, None)
            elif (len(graphinfo) == 6):
                graphinfo.insert(6, None)
            else:
                pass
            #self.cursor.execute("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?)", graphinfo)
       	    print graphinfo 
            self.connection.commit()
        self.cursor.close()

    def infogetting(self, pathdb1, pathdb2):
        self.hp_conn = sqlite3.connect(pathdb1)
        c = self.hp_conn.cursor()
    
        cc_conn = sqlite3.connect(pathdb2)
        d = cc_conn.cursor()
    
        c.execute("""Select * from events where module="rfi" """)
        rfiall = []
        
        for row in c:
	    print row
            rfilist=[]
            rfilist.append(row[2])
            rfilist.append(row[3].split(":")[0])
            protocal_pattern = re.compile("=(ht|f)tps?", re.IGNORECASE)
            matched_protocol = protocal_pattern.search(row[4]).group(0)
            injected_url = matched_protocol + row[4].partition(matched_protocol)[2].split("?")[0]
	    rfilist.append(injected_url.strip("="))   

            rfilist.append(row[5])
            print row[5] 
            print "row[6]="+row[6]
	    d.execute('select irc_addr, irc_channel from Botnets where file_md5=?', (row[6],))
            for row2 in d:
		rfilist.append(row2[0])
                rfilist.append(row2[1])
        
            rfiall.append(rfilist)
	   # print "rfiall="+str(rfiall)
        return rfiall
        
