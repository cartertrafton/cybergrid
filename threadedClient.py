import time
import threading
import queue
from gui.gui import *
from openPMUThreadsV2 import *
import pmuThreads
import pyshark


#
### adapted from
# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch09s07.html


### threadedClient class; launches GUI and worker thread
class ThreadedClient:

    #### start GUI and async threads; main thread
    def __init__(self, parent):
        self.parent = parent
        self.running = True

        # Create the queue
        self.queue = queue.Queue()
        self.queue.maxsize = 1
        # Set up the GUI part
        self.gui = GUI(parent, self.queue)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary

        # self.thread1 = threading.Thread(target=self.workerThreads)
        # self.thread1.start()
        self.thread0 = PMUrun(1, '127.0.0.1', 1410, 2048, True, self.queue)
        self.thread1 = PDCrun(1, '127.0.0.1', 1410, 2048, self.queue)
        # self.thread2 = ptpThread(interface='enp3s0',dispfilter='ptp',queue= self.queue)
        # self.thread2 = threading.Thread(target=self.ptp_worker, kwargs={'interface': 'enp3s0', 'df': 'ptp'})

        # Start the periodic call in the GUI to check if the queue contains
        # self.thread2.start()
        self.ts_buffer = list()
        self.thread0.start()
        sleep(0.001)
        self.thread1.start()

        # anything
        self.periodicCall()

    #### check queue and update GUI
    def periodicCall(self):
        if not self.queue.empty():
            buff = self.queue.get(block=True)
            print(' Length:',len(buff),' Min:',min(buff),' Max:',max(buff))

        self.gui.update_GUI()
        self.gui.processIncoming()
        self.parent.after(500, self.periodicCall)

    # def ptp_worker(self, interface=None, df=None):
    #     p = ptpSniffer()
    #     pack_list = []
    #     cap = pyshark.LiveCapture(interface='enp3s0', display_filter='ptp')
    #     while self.running:
    #         for pak in cap.sniff_continuously(packet_count=5):
    #             ob = p.assignPack(pak)
    #             pack_list.append(ob)
    #             # print(ob.mesType)
    #         for pk in pack_list:
    #             print(pk.mesType)
    #         print("--------\n")
    #         pack_list.clear()

