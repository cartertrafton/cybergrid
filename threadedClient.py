from gui.gui import *
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
cap = pyshark.LiveCapture(interface='enp3s0', display_filter='ptp')

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

        self.thread0 = PMUrun(1, '127.0.0.1', 1410, 2048, True)
        self.thread1 = PDCrun(1, '127.0.0.1', 1410, 2048, self.qev1, self.qLock1)
        self.thread2 = PMUrun(2, '127.0.0.1', 1420, 2048, True)
        self.thread3 = PDCrun(2, '127.0.0.1', 1420, 2048, self.qev2, self.qLock2)

        # Start the periodic call in the GUI to check if the queue contains
        # self.thread2.start()
        self.avgDelay = list()
        self.thread0.start()
        self.thread2.start()
        sleep(0.001)
        self.thread1.start()
        self.thread3.start()
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        ts1 = False
        ts2 = False
        try:
            #
            self.ptpCapture()

            if self.qev1.isSet():
                self.qLock1.acquire()
                if len(self.thread1.ts_buffer) > 0:
                    buff1 = self.thread1.ts_buffer.copy()
                    ts1 = True
                self.qLock1.release()
                self.qev1.clear()

            if self.qev2.isSet():
                self.qLock2.acquire()
                if len(self.thread3.ts_buffer) > 0:
                    buff2 = self.thread3.ts_buffer.copy()
                    ts2 = True
                self.qLock2.release()
                self.qev2.clear()

            if ts1 and ts2:
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
                ptpDelay = max(buff1)-self.ptp_buffer[0].tsComplete
                self.avgDelay.append(ptpDelay)
                print('-------------\n')
                print('Average Delay of PTP synchronization:', sum(self.avgDelay) / len(self.avgDelay))
                self.ptp_buffer.clear()
            else:
                pass
            self.gui.update_GUI()
            self.ptp_buffer.clear()
            self.gui.processIncoming()

        except UnboundLocalError or ValueError as e:
            print(e)
            self.parent.after(round((1000 * (1 / self.thread1.data_rate))), self.periodicCall)

        finally:
            if not self.running:
                # This is the brutal stop of the system. You may want to do
                # some cleanup before actually shutting it down.

                import sys
                sys.exit(1)
            self.parent.after(round((1000 * (1 / self.thread1.data_rate))), self.periodicCall)
            # self.parent.after(5, self.periodicCall)



    def ptpCapture(self):
        for pak in cap.sniff_continuously(packet_count=5):
            self.ptp_buffer.append(p.assignPack(pak))

        cap.clear()


    def endApplication(self):
        self.running = 0
