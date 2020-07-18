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

    def __init__(self, pdcid, pdcip, port, buffsize, qev, lock):
        self.pdc_id = pdcid
        self.pdc_ip = pdcip
        self.port = port
        self.buff_size = buffsize
        self.send = False
        self.ts_buffer = list()
        # self.data_buffer = list()
        self.data_rate = pmuThreads.cybergridCfg.get_data_rate()
        self.event = qev
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
                        if not self.event.isSet():
                            self.event.set()
                            self.ts_buffer = dataOut.copy()
                            self.qLock.release()
                    finally:
                        # print(self.queue, self.queue.qsize(), 'send', len(dataOut), self.queue.full())
                        dataOut.clear()
                        seq = 0


### adapted from
# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch09s07.html

p = ptpSniffer()
pack_list = []
#cap = pyshark.LiveCapture(interface='enp3s0', display_filter='ptp')

### threadedClient class - launches GUI and worker threads
class ThreadedClient:

    #### start GUI, set up and start PMU/PDC, and connect to PTP network
    def __init__(self, parent):
        self.parent = parent

        # Create the queue
        self.queue = queue.Queue(1)
        # self.queue.maxsize = 1
        self.qLock1 = threading.Lock()
        self.qLock2 = threading.Lock()
        self.qev1 = threading.Event()
        self.qev2 = threading.Event()

        # Set up the GUI part
        self.gui = GUI(parent, self.queue)
        self.ptp_buffer = list()
        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        # self.thread1 = threading.Thread(target=self.workerThreads)
        # self.thread1.start()
        self.thread0 = PMUrun(1, '127.0.0.1', 1410, 2048, True)
        self.thread1 = PDCrun(1, '127.0.0.1', 1410, 2048, self.qev1, self.qLock1)
        self.thread2 = PMUrun(2, '127.0.0.1', 1420, 2048, True)
        self.thread3 = PDCrun(2, '127.0.0.1', 1420, 2048, self.qev2, self.qLock2)
        # self.thread2 = ptpThread(interface='enp3s0',dispfilter='ptp',queue= self.queue)
        # self.thread2 = threading.Thread(target=self.ptp_worker, kwargs={'interface': 'enp3s0', 'df': 'ptp'})
        # Start the periodic call in the GUI to check if the queue contains
        # self.thread2.start()
        self.ts_buffer = list()
        self.thread0.start()
        self.thread2.start()
        sleep(0.001)
        self.thread1.start()
        self.thread3.start()
        # anything
        self.periodicCall()

    def periodicCall(self):
        self.gui.update_GUI()
        # self.thread1.ts_buffer.clear()
<<<<<<< HEAD
        #self.ptpCapture()
        # for pack in self.ptp_buffer:
        #     print(pack.mesType, '- time: ', pack.tsComplete)
        #
        # print('-------------')
        #self.ptp_buffer.clear()
=======

        self.ptp_buffer.clear()
>>>>>>> 409810a06832e529731c94c5afad880ff701e055
        self.gui.processIncoming()

        try:
            # print(self.thread1.queue, self.thread1.queue.qsize(), 'recv', self.thread1.queue.full())
            self.ptpCapture()
            if self.qev1.isSet():
                self.qLock1.acquire()

                buff1 = self.thread1.ts_buffer.copy()

                self.qLock1.release()
                self.qev1.clear()

            if self.qev2.isSet():
                self.qLock2.acquire()

                buff2 = self.thread3.ts_buffer.copy()

                self.qLock2.release()
                self.qev2.clear()

                print('PMU 1\n-------------------------')
                print(' Length:', len(buff1), ' Min:', min(buff1), ' Max:', max(buff1))
                print(' Time Delta:', max(buff1) - min(buff1))
                print('PMU 2\n-------------------------')
                print(' Length:', len(buff2), ' Min:', min(buff2), ' Max:', max(buff2))
                print(' Time Delta:', max(buff2) - min(buff2))

                print('Time Differences- max:', max(buff1)-max(buff2),'min:',min(buff1)-min(buff2))
            print('-------------')
            for pack in self.ptp_buffer:
                print(pack.mesType, '- time: ', pack.tsComplete)

            print('-------------\nptp delayed:',((max(buff1)+max(buff2))/2)-self.ptp_buffer[0].tsComplete,'\n\n')
            self.ptp_buffer.clear()

        except UnboundLocalError or ValueError as e:
            print(e)

        if not self.running:
            import sys
            sys.exit(1)
        self.parent.after(round((1000 * (1 / self.thread1.data_rate))), self.periodicCall)
        # self.parent.after(5, self.periodicCall)


    def ptpCapture(self):
<<<<<<< HEAD
        for pak in cap.sniff_continuously(packet_count=5):
=======

        for pak in cap.sniff_continuously(packet_count=1):
>>>>>>> 409810a06832e529731c94c5afad880ff701e055
            self.ptp_buffer.append(p.assignPack(pak))
        cap.clear()


    def endApplication(self):
        self.running = 0
