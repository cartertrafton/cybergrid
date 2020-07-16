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

p = ptpSniffer()
pack_list = []
cap = pyshark.LiveCapture(interface='enp3s0', display_filter='ptp')

### threadedClient class
class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """

    # this client launches GUI and worker thread
    def __init__(self, parent):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.parent = parent

        # Create the queue
        self.queue = queue.Queue()
        self.queue.maxsize = 1
        # Set up the GUI part
        self.gui = GUI(parent, self.queue)
        self.ptp_buffer = list()
        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
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

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        if self.queue.full():
            buff = self.queue.get()
            if len(buff) > 0:
                print(' Length:', len(buff), ' Min:', min(buff), ' Max:', max(buff))
                print(' Time Delta:', max(buff) - min(buff))

        self.ptpCapture()
        for pack in self.ptp_buffer:
            print(pack.mesType, '- time: ', pack.tsComplete)

        print('-------------')
        self.ptp_buffer.clear()
        self.gui.update_GUI()
        self.gui.processIncoming()


        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)

        self.parent.after(round((1000 * (1 / self.thread1.data_rate))), self.periodicCall)
        # self.parent.after(10, self.periodicCall)


    def ptpCapture(self):

        for pak in cap.sniff_continuously(packet_count=5):
            self.ptp_buffer.append(p.assignPack(pak))

        cap.clear()


    def endApplication(self):
        self.running = 0
