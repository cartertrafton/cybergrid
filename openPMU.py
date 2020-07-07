import subprocess as sp
import sys
import _thread as t
from ptpSniffer import ptpSniffer
import time

pmuCall1 = 'python3 pmuNet.py PMU 1 localhost 1410 512 true'
pdcCall1 = 'python3 pmuNet.py PDC 1 localhost 1410 512 true'

proc1 = sp.Popen(pmuCall1, shell=True, stdout=sp.PIPE)
time.sleep(0.1)
proc3 = sp.Popen(pdcCall1, shell=True, stdout=sp.PIPE)


#proc2 = sp.Popen(pmuCall2, shell=True, stdout=sp.PIPE)
#proc4 = sp.Popen(pdcCall2, shell=True, stdout=sp.PIPE,)

# sniff = ptpSniffer('enp3s0')

while True:
    try:
        output = proc3.stdout.readline()
        o2 = proc1.stdout.readline()

        if output == '' and proc3.poll() is not None:
            break
        if output:
            print(output.strip(),'\n\t',o2.strip())
        # if proc3.stderr.readline():
        #     proc1.stdout.close()
        #     proc3.stdout.close()
        #     proc1.kill()
        #     proc3.kill()
        #     sys.exit()
        rc = proc3.poll()
        # sniff.capture()
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
        sys.exit()