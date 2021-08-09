import subprocess
import array
from random import choices



class cleaner:
    def __init__(self):
        self.list = []
        self.last = ''
        self.hashes = []
        self.sizes = []
        self.packages = []
        self.black_list = ['org.pocketworkstation.pckeyboard']
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
        self.last = task
    def randomKill(self):
        self.killOne(choices(self.list)[0])
    def checkAndKill(self):
        self.getList()
        print(self.list)
        self.randomKill()
        print(self.last)
        print(len(self.list))
    def brutality(self):
        self.listPackages()
        while True:
            self.checkAndKill()

test = cleaner()
test.brutality()
