import subprocess
import os
pmuCall = 'PMU 1 127.0.0.1 1410 2048 true'
pdcCall = 'PDC 1 127.0.0.1 1410 2048 true'

print(pmuCall)
print(pdcCall)

os.system('gnome-terminal -x python3 pmuNet.py PMU 1 127.0.0.1 1410 2048 true')
