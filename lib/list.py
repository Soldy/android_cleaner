import copy
import array
import hashlib
from random import choices



class listClass:
   def __init__(self):
       self._apps =[]
       self._hashes = {}
       self._sizes = []
       self._packages = []
       self._safes = []
       self._priorities = []
       self._killed = []
       self._history = []
       self._whites = []
   def appClean(self):
       self._apps = []
   def appHash(self):
      return self.hash(
          ''.join(self._apps)
      )
   def hash(self, text):
      return hashlib.sha3_512(
          text.encode('utf8')
      ).hexdigest()
   def appLen(self):
      return len(self._apps)
   def appList(self):
      return copy.deepcopy(self._apps)
   def appAppend(self, app):
      if ':' in app:
          app = (app.split(':'))[0]
      if app not in self._packages:
          return
      if app not in self._apps:
         self._apps.append(copy.deepcopy(app))
         self._apps = sorted(self._apps)
   def hashAppend(self, has, app, save):
      if has not in self._hashes:
          self._hashes[has] = {}
      self._hashes[has][app]=save
   def historyAppend(self, app):
      self._history.append(copy.deepcopy(app))
   def killedAppend(self, app):
      if app not in self._killed:
          self._killed.append(copy.deepcopy(app))
   def killedGet(self):
      return copy.deepcopy(self._killed)
   def killedLast(self):
      return copy.deepcopy(
          self._killed[(len(self._killed)-1)]
      )
   def killed(self, app):
      self.historyAppend(app)
      self.killedAppend(app)
   def packageClean(self):
       self._packages = []
   def packageAppend(self, app):
      app = app.rstrip()
      if app not in self._packages:
          self._packages.append(copy.deepcopy(app))
          self._packages = sorted(self._packages)
   def priorityAppend(self, app):
      if app not in self._priorities:
          self._priorities.append(copy.deepcopy(app))
   def priorityUpdate(self):
      self._priorities = []
      for app in self._safes:
          if app not in self._killed:
              self.priorityAppend(app)
   def priorityGet(self):
      return copy.deepcopy(self._priorities)
   def priorityLen(self):
      return len(self._priorities)
   def priorityRandom(self):
      return copy.deepcopy(choices(self._priorities)[0])
   def safeAppend(self, app):
      if app not in self._safes:
           self._safes.append(copy.deepcopy(app))
   def safeUpdate(self):
      self._safes = []
      for app in self._apps:
          if app not in self._whites:
              self.safeAppend(app)
   def safeLen(self):
      return len(self._safes)
   def safeRandom(self):
      return copy.deepcopy(choices(self._safes)[0])
   def safeGet(self):
      return copy.deepcopy(self._safes)
   def whiteInit(self, white):
       self._whites = copy.deepcopy(white)

