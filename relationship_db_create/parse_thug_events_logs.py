#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import xml.dom.minidom
import json
import re
import logging
import sys
import os

import xpsql

DBDIR = './db/'

if not os.path.exists(DBDIR):
    os.mkdir(DBDIR)

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

log       = logging.getLogger('xp.log')
handler   = logging.FileHandler('xp.logs')
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.INFO)

doc = ''
fd = open('thug_events.logs', 'r')
for i in fd:
    doc += i.strip()
fd.close()

xdb = xpsql.xml_DB()

nc = re.findall(r'<MAEC_Bundle.*?</MAEC_Bundle>', doc)
for nnc in nc:
    url = []; url_from = []; edge = []; files = [];
    cve = []; link = []; file_md5 = []; xid = 0; count = 0
    url_oid = []
    try:
        d = xml.dom.minidom.parseString(nnc)
    except xml.parsers.expat.ExpatError:
        print >> sys.stderr, "Parsing xml failed!!"
        continue
    intime = d.getElementsByTagName('Analysis')[0].getAttribute('start_datetime')
    for n in d.getElementsByTagName('Text'):
        tt = getText(n.childNodes)
        if 'URL' in tt:
	    count += 1
	    try:
                url.append(tt.split(' ')[2])
                xdb.insert('objects', (None, tt.split(' ')[2], 'Landding site' if count == 1 else 'hopping site'))
            except IndexError:
                print >> sys.stderr, 'URL:', tt
                continue
            try:
                url_from.append(tt.split(' ')[6].strip(')'))
            except IndexError:
                print >> sys.stderr, 'URL_FROM:', tt
	        continue
    if count == 0:
        url.append(None)
    else:
        xdb.insert('xml', (None, url[0], intime))
        xid = xdb.seek('SELECT xid FROM xml WHERE url = "%s"' % url[0])
    for u in url:
        oid = xdb.seek('SELECT oid FROM objects WHERE content = "%s"' % u)
        url_oid.append(oid)
    print >>sys.stderr, 'url_oid', url_oid

    for n in d.getElementsByTagName('File_System_Object_Attributes'):
        here_type = n.getElementsByTagName('File_Type')[0].getAttribute('type')
        here_md5 = ''
        for m in n.getElementsByTagName('Hash'):
            if 'md5' == m.getAttribute('type'):
                here_md5 = getText(m.getElementsByTagName('Hash_Value')[0].childNodes)
        files.append({'type': here_type, 'md5': here_md5})
        xdb.insert('objects', (None, here_md5, here_type))
    for b in d.getElementsByTagName('Behavior'):
        if len(b.getElementsByTagName('Purpose')) != 0:
            n = b.getElementsByTagName('Known_Exploit')[0]
            cve.append(n.getAttribute('cve_id'))
            desc = getText(b.getElementsByTagName('Text')[0].childNodes)
            xdb.insert('vulnerability', (None, n.getAttribute('cve_id'), desc))
    for e in range(len(url_from)):
        if 'None' != url_from[e]:
	    try:
	        edge.append(list((url.index(url_from[e]), e)))
	    except ValueError:
                print >> sys.stderr, 'No from site found', url_from[e]
                edge.append(list((0, e)))
	        continue
    sd = {"xid" : xid,
          "timestamp" : intime,
          "url" : url[0],
          "nodes" : [ x for x in url[1:] ],
          "edges" : [ i for i in edge ],
          "file" : [ m for m in files ],
          "cve" : [ c for c in cve]}
    print str(json.dumps(sd))
    log.info(str(json.dumps(sd)))

del xdb
