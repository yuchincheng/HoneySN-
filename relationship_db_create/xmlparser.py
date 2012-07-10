#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3
import sys

class xml_DB(object):
    def __init__(self):
        self.conn = sqlite3.connect('./db/events.db')
        self.create()
        self.sql_x = "INSERT INTO xml VALUES(?, ?, ?)"
        self.sql_o = "INSERT INTO objects VALUES(?, ?, ?)"
        self.sql_v = "INSERT INTO vulnerability VALUES(?, ?, ?)"
        self.sql_r = "INSERT INTO relations VALUES(?, ?, ?, ?, ?)"

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create(self):
        self.cur = self.conn.cursor()
        table_names = ['xml', 'objects', 'vulnerability', 'relations']
        self.cur.execute("""CREATE TABLE IF NOT EXISTS xml (xid INTEGER PRIMARY KEY, url TEXT, timestamp TEXT)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS objects (oid INTEGER PRIMARY KEY, content TEXT, type text)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS vulnerability (vid INTEGER PRIMARY KEY, cve_id TEXT, description TEXT)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS relations (rid INTEGER PRIMARY KEY, fromId TEXT, toId TEXT, comments TEXT, timestamp TEXT)""")
        self.conn.commit()
        self.cur.close()

    def insert(self, tname, data):
        if self._checkUnique(tname, data[1]) != 0:
            return
        if 'xml' == tname:
            sql = self.sql_x
        if 'relations' == tname:
            sql = self.sql_r
        if 'vulnerability' == tname:
            sql = self.sql_v
        if 'objects' == tname:
            sql = self.sql_o
        self.cur = self.conn.cursor()
        try:
            self.cur.execute(sql, data)
        except sqlite3.OperationalError, e:
            print "Insert into database Error:", e
        except sqlite3.ProgrammingError, e:
            print "Insert into database Error:", e
        self.conn.commit()
        self.cur.close()

    def seek(self, sql):
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        res = self.cur.fetchall()
        self.cur.close()
        return res

    def _checkUnique(self, tname, data):
        if tname == 'objects':
            cname = 'content'
        if tname == 'vulnerability':
            cname = 'cve_id'
        if tname == 'xml':
            cname = 'url'
        if tname == 'relations':
            return 0
        self.cur = self.conn.cursor()
        sql = """SELECT * FROM %s WHERE %s = '%s'""" % (tname, cname, data)
        ns = []
        try:
            ns = self.cur.execute(sql).fetchall()
        except sqlite3.OperationalError, e:
            print >> sys.stderr, 'inner sqlite op', e, data
        self.cur.close()
        return len(ns)

