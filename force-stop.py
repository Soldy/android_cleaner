import subprocess
import array
from random import choices



class cleaner:
    def __init__(self):
        self.list = []
        self.last = ''
        self.hashes = []
        self.sizes = []
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
            if ('com' in last or 'android' in last) and '.' in last and ':' not in last:
                self.list.append(last)
        self.list = sorted(self.list)
        proc.wait()
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
        while True:
            self.checkAndKill()

test = cleaner()
test.brutality()
