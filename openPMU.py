import subprocess
import os
import sys

if sys.platform == "linux":
    print("linux")
    cmdP = 'gnome-terminal -x'
elif sys.platform == 'win32':
    print("windows")
    cmdP = 'cmd'

pmuCall = 'PMU 1 127.0.0.1 1410 2048 true'
pdcCall = 'PDC 1 127.0.0.1 1410 2048 true'

os.system(cmdP + ' python3 pmuNet.py PMU 1 localhost 1410 2048 true')
os.system(cmdP + ' python3 pmuNet.py PDC 1 localhost 1410 2048 true')
os.system(cmdP + ' python3 pmuNet.py PMU 2 localhost 1420 2048 true')
os.system(cmdP + ' python3 pmuNet.py PDC 2 localhost 1420 2048 true')