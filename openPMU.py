import subprocess as sp
import os
import sys

if sys.platform == "linux":
    print("linux")
    cmdP = 'gnome-terminal -e'
elif sys.platform == 'win32':
    print("windows")
    cmdP = 'cmd'

pmuCall1 = cmdP + ' "python3 pmuNet.py PMU 1 localhost 1410 2048 true"'
pdcCall1 = cmdP + ' "python3 pmuNet.py PDC 1 localhost 1410 2048 true"'

pmuCall2 = cmdP + ' "python3 pmuNet.py PMU 2 localhost 1420 2048 true"'
pdcCall2 = cmdP + ' "python3 pmuNet.py PDC 2 localhost 1420 2048 true"'

proc1 = sp.Popen(pmuCall1, shell=True)
proc2 = sp.Popen(pmuCall2, shell=True)
proc3 = sp.Popen(pdcCall1, shell=True)
proc4 = sp.Popen(pdcCall2, shell=True)

