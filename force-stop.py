import subprocess
from random import choices

killable =[]
p = subprocess.Popen('adb shell ps', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    parts = line.split()
    last = parts[len(parts)-1].decode('utf-8')
    if ('com' in last or 'android' in last) and '.' in last and ':' not in last:
        killable.append(last)
print(killable);
print(len(killable));
retval = p.wait()
c = (
    'adb shell am force-stop '+choices(killable)[0]
)
print(c)
k = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print(k)
print(k.wait())
