import time
import threading
import queue
from gui.gui import *
# from openPMUThreadsV2 import *
import pmuThreads
import pyshark
from ptpSniffer import ptpSniffer, ptpPacketData
from threading import Thread
from time import sleep


class PMUrun(Thread):
    def __init__(self, pmuid, pmuip, port, buffsize, setTS):
        self.pmu_id = pmuid
        self.pmu_ip = pmuip
        self.port = port
        self.buff_size = buffsize
        self.set_TS = setTS
        self.queue = queue
        Thread.__init__(self)
        self.daemon = True
        self.output = None
        # self.start()

    def run(self):
        print("Starting PMU " + str(self.pmu_id) + "\n")
        pmuThreads.pmuThread(self.pmu_id, self.pmu_ip, self.port, self.buff_size, self.set_TS)


class PDCrun(Thread):

    def __init__(self, pdcid, pdcip, port, buffsize, queue, lock):
        self.pdc_id = pdcid
        self.pdc_ip = pdcip
        self.port = port
        self.buff_size = buffsize
        self.send = False
        self.ts_buffer = list()
        # self.data_buffer = list()
        self.data_rate = pmuThreads.cybergridCfg.get_data_rate()
        self.queue = queue
        self.qLock = lock
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        seq = 0
        dataOut = list()
        print("Starting PDC " + str(self.pdc_id) + "\n")
        while self.isAlive():
            for out in pmuThreads.pdcThread(self.pdc_id, self.pdc_ip, self.port, self.buff_size):
                if seq < self.data_rate:
                    self.send = False
                    dataOut.append(out['time'])
                    seq+=1
                elif seq == self.data_rate:
                    self.qLock.acquire()

                    try:
                        if not self.queue.full():
                            queueEvent.set()
                            self.ts_buffer = dataOut.copy()
                            self.queue.put_nowait(dataOut.copy())
                            self.qLock.release()
                    finally:
                        # print(self.queue, self.queue.qsize(), 'send', len(dataOut), self.queue.full())
                        dataOut.clear()
                        seq = 0


#
### adapted from
# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch09s07.html

p = ptpSniffer()
pack_list = []
cap = pyshark.LiveCapture(interface='enp3s0', display_filter='ptp')
queueEvent = threading.Event()

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
        self.queue = queue.Queue(1)
        # self.queue.maxsize = 1
        self.qLock = threading.Lock()
        # Set up the GUI part
        self.gui = GUI(parent, self.queue)
        self.ptp_buffer = list()
        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        # self.thread1 = threading.Thread(target=self.workerThreads)
        # self.thread1.start()
        self.thread0 = PMUrun(1, '127.0.0.1', 1410, 2048, True)
        self.thread1 = PDCrun(1, '127.0.0.1', 1410, 2048, self.queue, self.qLock)
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
        # print('test')
        self.gui.update_GUI()
        # self.thread1.ts_buffer.clear()
        self.ptpCapture()
        # for pack in self.ptp_buffer:
        #     print(pack.mesType, '- time: ', pack.tsComplete)
        #
        # print('-------------')
        self.ptp_buffer.clear()
        self.gui.processIncoming()

        try:
            self.qLock.acquire()
            # print(self.thread1.queue, self.thread1.queue.qsize(), 'recv', self.thread1.queue.full())
            if queueEvent.isSet():
                buff = self.thread1.ts_buffer.copy()
                # self.thread1.ts_buffer.clear()
                queueEvent.clear()
            self.qLock.release()
            # print('we getting this?')
            print(len(buff))
            print(' Length:', len(buff), ' Min:', min(buff), ' Max:', max(buff))
            print(' Time Delta:', max(buff) - min(buff))
        except UnboundLocalError as e:
            print(e)

        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.parent.after(round((1000 * (1 / self.thread1.data_rate))), self.periodicCall)
        # self.parent.after(1000, self.periodicCall)


    def ptpCapture(self):

        for pak in cap.sniff_continuously(packet_count=5):
            self.ptp_buffer.append(p.assignPack(pak))

        cap.clear()


    def endApplication(self):
        self.running = 0
