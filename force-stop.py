import subprocess
import array
import time
import sqlite3
import lib.configread as __config
import lib.list as listC
from random import choices


print(__config.whiteList())
_list = listC.listClass()
_list.whiteInit(__config.whiteList())

class cleaner:
    def __init__(self):
        self.listPackages()
        self.getList()
    def listPackages(self):
        _list.packageClean()
        proc = subprocess.Popen(
            'adb shell pm list packages',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        for line in proc.stdout.readlines():
            line = line.decode('utf-8')
            parts = line.split(':')
            _list.packageAppend(parts[1])
        proc.wait()
    def getList(self):
        _list.appClean()
        proc = subprocess.Popen(
            'adb shell ps',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        for line in proc.stdout.readlines():
            parts = line.split()
            last = parts[len(parts)-1].decode('utf-8')
            _list.appAppend(last)
        _list.safeUpdate()
        _list.priorityUpdate()
        proc.wait()
    def killOne(self, app):
        save = {}
        self.getList()
        has = _list.appHash()
        save['before'] = _list.appLen()
        command = (
           'adb shell am force-stop '+app
        )
        kill = subprocess.Popen(
           command, 
           shell=True,
           stdout=subprocess.PIPE,
           stderr=subprocess.STDOUT
        )
        kill.wait()
        _list.killed(app)
        self.getList()
        save['after'] = _list.appLen()
        _list.hashAppend(has, app, save)
        return save
    def randomKill(self):
        if _list.priorityLen() > 0 :
            return self.killOne(_list.priorityRandom())
        return self.killOne(_list.safeRandom())
    def checkAndKill(self):
        self.getList()
        print(_list.appList())
        print(self.randomKill())
        print(_list.killedLast())
        print(_list.appLen())
    def brutality(self):
        while True:
            self.checkAndKill()
            time.sleep(2)
    def priority(self):
        print(_list.safeLen())
        print(_list.priorityLen())
        while (_list.priorityLen()>0):
            self.checkAndKill()
            time.sleep(2)



test = cleaner()
test.priority()

