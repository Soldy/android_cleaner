
class smartDatabase:
   def __init__(self):
       self.con = sqlite3.connect('deviceKnowladge.db')
       self.cur = self.con.cursor()
       self.create()
   def create(self):
       self.cur.execute(
           '''CREATE TABLE IF NOT EXISTS kill_try
              (hash TEXT, app TEXT, before INTEGER, after INTEGER)'''
       )
       self.con.commit()
   def saveKill(self, hash_, app_, before, after):
       self.cur(
           "INSERT INTO kill_try VALUES ('"+hash_+"', '"+app_+"', '"+str(before)+"', '"+str(after)+"')"
       )
       self.con.commit()
   def getKillProcess(self, hash_, app_):
       cur.execute("SELECT * FROM kill_try WHERE  hash =  ? AND app = ?", (hash_, app_))
       return cur.fetchall()
   def getKill(self, hash_):
       cur.execute("SELECT * FROM kill_try WHERE  hash =  ?", (hash_))
       return cur.fetchall()
   def getApps(self, hash_):
       list_ = []
       for row in cur.execute("SELECT * FROM kill_try WHERE  hash =  ?", (hash_)):
           list_.append(row[1])

import sqlite3
