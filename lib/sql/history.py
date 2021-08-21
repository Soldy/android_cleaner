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
   def check(self, hash_, app_):
       self.cur.execute(
           "SELECT * FROM kill_history WHERE hash = :hash AND app = :app ",
           {
               "hash":hash_,
               "app":app_
           }
       )
       if len(self.cur.fetchall()) > 0:
           return True
       return False
   def get(self, hash_, app_):
       self.cur.execute(
           "SELECT * FROM kill_history WHERE hash = :hash AND app = :app ",
           {
               "hash":hash_,
               "app":app_
           }
       )
       return self.cur.fetchall()
   def getApp(self, app_):
       self.cur.execute(
           "SELECT * FROM kill_history WHERE app = ? ",
           app_
       )
       return self.cur.fetchall()
   def get(self, hash_):
       self.cur.execute(
           "SELECT * FROM kill_history WHERE hash = ? ",
           hash_
       )
       return self.cur.fetchall()

