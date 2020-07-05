import time
import pmuThreads
from threading import Thread


class PMUrun(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        pmuThreads.pmuThread(1, '127.0.0.1', 1410, 2048, True)
class PDCrun(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        pmuThreads.pdcThread(1, '127.0.0.1', 1410, 2048)

PMUrun()
time.sleep(0.1)
PDCrun()
while True:
    pass
