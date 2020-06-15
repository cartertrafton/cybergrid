import subprocess
import os
import sys

if sys.platform == "linux":
    cmdP = 'gnome-terminal -x'
elif sys.platform == 'win32':
    cmdP = 'cmd'

pmuCall = 'PMU 1 127.0.0.1 1410 2048 true'
pdcCall = 'PDC 1 127.0.0.1 1410 2048 true'

os.system(cmdP + ' python3 pmuNet.py PMU 1 127.0.0.1 1410 2048 true')
os.system(cmdP + ' python3 pmuNet.py PDC 1 127.0.0.1 1410 2048 true')
os.system(cmdP + ' python3 pmuNet.py PMU 2 127.0.0.1 1420 2048 true')
os.system(cmdP + ' python3 pmuNet.py PDC 2 127.0.0.1 1420 2048 true')