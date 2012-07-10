import re
import sqlite3

#This code is for building up rfigraph.db from gastopf.db and sandbox.db

#connection = sqlite3.connect("rfigraph.db")
    
    
""" 
	def insert(self, itemall):
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
            self.cursor.execute("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?)", graphinfo)
        
        self.connection.commit()
        self.cursor.close()
"""
 #self, pathdb1, pathdb2):
hp_conn = sqlite3.connect("../pool/db/glastopf.db")
c=hp_conn.cursor()
    
#cc_conn = sqlite3.connect("../pool/db)
#        d = cc_conn.cursor()
    
c=hp_conn.execute("""Select * from events where module="rfi" """)
rfiall = []
        
for row in c:
	rfilist=[]
	rfilist.append(row[1])
	rfilist.append(row[2].split(":")[0])
        
	protocal_pattern = re.compile("=(ht|f)tps?", re.IGNORECASE)
	matched_protocol = protocal_pattern.search(row[3]).group(0)
	injected_url = matched_protocol + row[3].partition(matched_protocol)[2].split("?")[0]
	rfilist.append(injected_url.strip("="))   

	rfilist.append(row[5]) 
#   	dd=sqlite3.connect("../pool/db/sandbox.sb")
#	dl=dd.cursor() 
#	dl.execute('select irc_addr, irc_channel from events where file_md5=?', (row[5],))
#	for row2 in dl:
#		rfilist.append(row2[0])
#                rfilist.append(row2[1])
        
#	dd.close()
#	rfiall.append(rfilist)
	print rfiall
hp_conn.close()
        
