import subprocess
import hashlib
import array
import time
import sqlite3
from random import choices



class cleaner:
    def __init__(self):
        self.list = []
        self.last = ''
        self.hashes = {}
        self.sizes = []
        self.packages = []
        self.safe_list = []
        self.priority_list = []
        self.black_list = ['org.pocketworkstation.pckeyboard']
        self.killed_list=[]
        self.killSize=[]
        self.listPackages()
        self.getList()
        print(self.list)
        print(self.safe_list)
        print(self.priority_list)
    def hash(self):
        return hashlib.sha3_512(
            ''.join(self.list).encode('utf8')
        ).hexdigest()
    def listPackages(self):
        self.packages = []
        proc = subprocess.Popen(
            'adb shell pm list packages',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        for line in proc.stdout.readlines():
            line = line.decode('utf-8')
            parts = line.split(':')
            self.packages.append(parts[1].rstrip())
        self.packages = sorted(self.packages)
        proc.wait()
    def getList(self):
        self.list = []
        proc = subprocess.Popen(
            'adb shell ps',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        for line in proc.stdout.readlines():
            parts = line.split()
            last = parts[len(parts)-1].decode('utf-8')
            if last in self.packages:
                self.listAppend(last)
        self.list = sorted(self.list)
        self.safeAppend()
        self.priorityAppend()
        proc.wait()
    def listAppend(self, task):
         if ':' in task:
             task = (task.split(':'))[0]
         if task not in self.list:
            self.list.append(task)
    def safeAppend(self):
        self.safe_list = []
        for app in self.list:
            if app not in self.black_list:
               self.safe_list.append(app)
    def priorityAppend(self):
        self.priority_list = []
        for app in self.safe_list:
            if app not in self.killed_list:
               self.priority_list.append(app)
    def killedAppend(self, app):
        if app not in self.killed_list:
           self.killed_list.append(app)
    def killOne(self, task):
        save = {}
        self.getList()
        has = self.hash()
        save['before'] = len(self.list)
        command = (
           'adb shell am force-stop '+task
        )
        kill = subprocess.Popen(
           command, 
           shell=True,
           stdout=subprocess.PIPE,
           stderr=subprocess.STDOUT
        )
        kill.wait()
        self.killedAppend(task)
        self.last = task
        self.getList()
        save['after'] = len(self.list)
        if has not in self.hashes:
            self.hashes[has] = {}
        self.hashes[has][task]=save
        return save
    def randomKill(self):
        if len(self.priority_list) > 0:
            return self.killOne(choices(self.priority_list)[0])
        return self.killOne(choices(self.safe_list)[0])
    def checkAndKill(self):
        self.getList()
        print(self.list)
        print(self.randomKill())
        print(self.last)
        print(len(self.list))
    def brutality(self):
        while True:
            self.checkAndKill()
            time.sleep(2)
    def priority(self):
        while (len(self.priority_list)>0):
            self.checkAndKill()
            time.sleep(2)



test = cleaner()
test.priority()
