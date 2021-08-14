import copy
import subprocess

def runner(command):
    proc = subprocess.Popen(
         command,
         shell=True,
         stdout=subprocess.PIPE,
         stderr=subprocess.STDOUT
    )
    out = copy.deepcopy(proc.stdout.readlines())
    proc.wait()
    return out
