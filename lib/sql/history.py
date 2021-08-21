import sqlite3



class historyDatabase:
   def __init__(self):
       self.con = sqlite3.connect('sql/history.db')
       self.cur = self.con.cursor()
       self.create()
   def create(self):
       self.cur.execute(
           '''CREATE TABLE IF NOT EXISTS kill_history
              (hash TEXT, app TEXT, result INTEGER)'''
       )
       self.con.commit()
   def kill(self, hash_, app_, result):
       self.cur.execute(
           "INSERT INTO kill_history VALUES (:hash, :app, :result )",
           {
               "hash":hash_,
               "app":app_,
               "result":result
           }
       )
       self.con.commit()

