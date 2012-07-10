import networkx as nx
import sqlite3
import matplotlib.pyplot as plt

class GraphFun():
    
    def __init__(self):
        self.nodelist = {}
        self.numlist =0
    
    def graphcreate(self):
        G = nx.Graph()
        return G
        
    def getsql(self, dbname):
        conn = sqlite3.connect(dbname)
        dbcursor = conn.cursor()
        dbcursor.execute(""" SELECT * from events """)
        return dbcursor.fetchall()
    
    def datagen(self, db_fetch, G):
        nodecolor = {2:'yellow', 3:'green', 4:'blue', 5:'red'}
        for nodeitem in db_fetch:
            for v in range(2,6):
                if nodeitem[v]:
                    if nodeitem[v] not in self.nodelist:
                        self.nodelist[nodeitem[v]] = self.numlist
                        G.add_node(self.numlist, color=nodecolor[v], count=0)
                        self.numlist += 1
                    else:
                        G.node[self.nodelist[nodeitem[v]]]['count'] +=1
            
    def addedge(self, db_fetch, G): 
        for edgeitem in db_fetch:
            if edgeitem[2] and edgeitem[3]:
                G.add_edge(self.nodelist[edgeitem[2]], self.nodelist[edgeitem[3]])
            if edgeitem[3] and edgeitem[4]:
                G.add_edge(self.nodelist[edgeitem[3]], self.nodelist[edgeitem[4]])
            if edgeitem[4] and edgeitem[5]:
                G.add_edge(self.nodelist[edgeitem[4]], self.nodelist[edgeitem[5]])
                
    def sngplot_degree (self, G):
        node_color=[G.node[v]['color'] for v in G]
        node_size=[(G.degree(v))*8 for v in G]
        nx.draw(G, pos=nx.spring_layout(G), node_size=node_size, node_color=node_color, vmin=0.0, vmax=1.0, with_labels=False)
    
    def sngplot_count (self, G):
        node_color=[G.node[v]['color'] for v in G]
        node_size=[float((G.node[v]['count'])) for v in G]
        nx.draw(G, pos=nx.spring_layout(G), node_size=node_size, node_color=node_color, vmin=0.0, vmax=1.0, with_labels=False)
    
    def cirplot (self, G):
        node_color=[G.node[v]['color'] for v in G]
        node_size=[(G.degree(v))*8 for v in G]
        nx.draw_circular(G, node_size= node_size, node_color=node_color, with_labels=False)
    
    def plotfig (self, G, titlestr, textstr):
        plt.figure(figsize=(8,8), dpi=96, facecolor='b', edgecolor='k')
        font = {'fontname':'Helvetica', 'color':'k', 'fontweight':'bold', 'fontsize':14}
        plt.title(titlestr, font)
        plt.text(0.5, 0.95, textstr, horizontalalignment='center', transform=plt.gca().transAxes, size='small')  
                
    def savefig (self, figname):
        plt.savefig(figname)