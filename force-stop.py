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
        self.list = {}
        self.sizes = []
        self.packages = []
        self.black_list = ['org.pocketworkstation.pckeyboard']
        self.killed=[]
        self.killSize=[]
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
                self.safeAppend(last)
        self.list = sorted(self.list)
        proc.wait()
    def safeAppend(self, task):
         if ':' in task:
             task = (task.split(':'))[0]
         if task not in self.black_list:
            self.list.append(task)
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
        self.killed.append(task)
        self.last = task
        self.getList()
        save['after'] = len(self.list)
        if has not in self.hashes:
            self.hashes[has] = {}
        self.hashes[has][task]=save
        return save
    def randomKill(self):
        return self.killOne(choices(self.list)[0])
    def checkAndKill(self):
        self.getList()
        print(self.list)
        print(self.randomKill())
        print(self.last)
        print(len(self.list))
    def brutality(self):
        self.listPackages()
        while True:
            self.checkAndKill()
            time.sleep(2)



test = cleaner()
test.brutality()
