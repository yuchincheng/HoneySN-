import graphgen
import sqldata
import os

if __name__ == '__main__':
    
    
    # Generate rfigraph.db from glastopf.db and sandbox.db
    
    sqlpoint = sqldata.LogSQLite()
    itemall = sqlpoint.infogetting("../pool/db/glastopf.db", "../pool/db/sandbox.db")
    sqlpoint.insert(itemall)
    sqlpoint.dbclose() 
    
    
    """
    classall = graphgen.GraphFun()
    G = classall.graphcreate()
    dbfetch = classall.getsql("rfigraph.db")
    classall.datagen(dbfetch, G)
    classall.addedge(dbfetch, G)
    figtitle = "RFI Events Collection and Analysis by Glaspot and PHPSandbox"
    textstr = "Yellow:Attacker IP, Green:RFI URL, Blue:RFI File MD5, Red:Botnet C&C IP"
    classall.plotfig (G, figtitle, textstr)
    classall.sngplot_count(G)
    classall.savefig ("figdir/rfisng_sngplot_count.png")
    """
    
    myclass = graphgen.GraphFun()
    H = myclass.graphcreate()
    dbfetch = myclass.getsql("rfigraph.db")
    myclass.datagen(dbfetch, H)
    myclass.addedge(dbfetch, H)
    figtitle = "RFI Events Collection and Analysis by Glaspot and PHPSandbox"
    textstr = "Yellow:Attacker IP, Green:RFI URL, Blue:RFI File MD5, Red:Botnet C&C IP"
    myclass.plotfig (H, figtitle, textstr)
    myclass.sngplot_degree(H)
    myclass.savefig ("figdir/rfisng_sngplot_degree_20120322.png")
    
    """
    myclass2 = graphgen.GraphFun()
    K = myclass2.graphcreate()
    dbfetch = myclass2.getsql("rfigraph.db")
    myclass2.datagen(dbfetch, K)
    myclass2.addedge(dbfetch, K)
    figtitle = "RFI Events Collection and Analysis by Glaspot and PHPSandbox"
    textstr = "Yellow:Attacker IP, Green:RFI URL, Blue:RFI File MD5, Red:Botnet C&C IP"
    myclass2.plotfig (K, figtitle, textstr)
    myclass2.cirplot(K)
    myclass2.savefig ("figdir/rfisng_cirplot_degree.png")
    """
