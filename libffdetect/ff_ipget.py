'''
Created on 2012/6/12

@author: Julia YuChin Cheng
'''

from BeautifulSoup import BeautifulSoup as Soup
import urllib
import re

def BFKInfo(domain):
    """
    @summary: Feed C&C domain to BFK (Passive DNS replication) service for gathering IPs
    @note: BFK Service: http://www.bfk.de/index.html
    
    """
    iplist= list()
    soup = Soup(urllib.urlopen('http://www.bfk.de/bfk_dnslogger_en.html?query='+domain+'#result'))
    table = soup.find("table", {"id":"logger"})
    for row in table.findAll("tr"):
        for anchor in row.findAll('a', {'href' : re.compile('.+')}):
            if anchor.string != domain:
                iplist.append(anchor.string)
                
    return iplist