import array
import time
import lib.configread as __config
import lib.list as listC
import lib.sql.history as historyC
from lib.runner import runner
from random import choices

_history = historyC.historyDatabase()
_list = listC.listClass()
_list.whiteInit(__config.whiteList())

class cleaner:
    def __init__(self):
        self.listPackages()
        self.getList()
    def listPackages(self):
        _list.packageClean()
        for line in runner(
            'adb shell pm list packages'
        ):
            _list.packageAppend(line.decode('utf-8').split(':')[1])
    def getList(self):
        _list.appClean()
        for line in runner(
            'adb shell ps',
        ):
            parts = line.split()
            _list.appAppend(parts[len(parts)-1].decode('utf-8'))
        _list.safeUpdate()
        _list.priorityUpdate()
    def killOne(self, app):
        save = {}
        self.getList()
        has = _list.appHash()
        save['before'] = _list.appLen()
        kill = runner(
           'adb shell am force-stop '+app
        )
        _list.killed(app)
        self.getList()
        save['after'] = _list.appLen()
        _list.hashAppend(has, app, save)
        _history.kill(
            has,
            _list.hash(app),
            (save['after']-save['before'])
        )
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

