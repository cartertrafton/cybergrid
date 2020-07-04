import subprocess as sp
import sys
import _thread as t
from ptpSniffer import ptpSniffer

if sys.platform == "linux":
    print("linux")
    cmdP = 'gnome-terminal -e'
elif sys.platform == 'win32':
    print("windows")
    cmdP = 'cmd'

pmuCall1 = 'python3 pmuNet.py PMU 1 localhost 1410 2048 true'
pdcCall1 = 'python3 pmuNet.py PDC 1 localhost 1410 2048 true'

pmuCall2 = cmdP + ' "python3 pmuNet.py PMU 2 localhost 1420 2048 true"'
pdcCall2 = cmdP + ' "python3 pmuNet.py PDC 2 localhost 1420 2048 true"'

proc1 = sp.Popen(pmuCall1, shell=True, stdout=sp.PIPE)
proc3 = sp.Popen(pdcCall1, shell=True, stdout=sp.PIPE)


#proc2 = sp.Popen(pmuCall2, shell=True, stdout=sp.PIPE)

#proc4 = sp.Popen(pdcCall2, shell=True, stdout=sp.PIPE,)
#sniff = ptpSniffer('enp3s0')

while True:
    try:

        output = proc3.stdout.readline()

        if output == '' and proc3.poll() is not None:
            break
        if output:
            print(output.strip())
        rc = proc3.poll()
        #sniff.capture()
    except BrokenPipeError:
        proc1.stdout.close()
        proc3.stdout.close()
        proc1.kill()
        proc3.kill()
        sys.exit()
    except KeyboardInterrupt:
        proc1.stdout.close()
        proc3.stdout.close()
        proc1.kill()
        proc3.kill()