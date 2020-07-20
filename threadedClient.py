from gui.gui import *
import pmuThreads
import pyshark
from ptpSniffer import ptpSniffer, ptpPacketData
from threading import Thread
from time import sleep
from datetime import datetime


# from hanging_threads import start_monitoring
# monitoring_thread = start_monitoring()

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
        self.data_buffer = list()
        self.data_rate = pmuThreads.cybergridCfg.get_data_rate()
        self.event = qev
        self.qLock = lock
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        seq = 0
        tsOut = list()
        measOut = list()
        print("Starting PDC " + str(self.pdc_id) + "\n")
        while self.is_alive():
            for out in pmuThreads.pdcThread(self.pdc_id, self.pdc_ip, self.port, self.buff_size):
                if seq < self.data_rate:
                    self.send = False
                    tsOut.append(out['time'])
                    measOut.append(out['measurements'])
                    seq += 1
                elif seq == self.data_rate:
                    if not self.event.isSet():
                        self.event.set()
                        self.qLock.acquire()

                        self.ts_buffer = tsOut.copy()
                        self.data_buffer = measOut.copy()
                        tsOut.clear()
                        measOut.clear()
                        seq = 0

                        self.qLock.release()

                        # print(self.queue, self.queue.qsize(), 'send', len(dataOut), self.queue.full())



### adapted from
# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch09s07.html

p = ptpSniffer()
pack_list = []
# cap = pyshark.LiveCapture(interface='enp3s0', display_filter='ptp')
cap = pyshark.LiveCapture(interface='wlp5s0', display_filter='ptp')


### threadedClient class - launches GUI and worker threads
class ThreadedClient:
    def __init__(self, parent):
        self.running = 1
        self.parent = parent
        self.queue = queue.Queue()
        self.qLock1 = threading.Lock()
        self.qLock2 = threading.Lock()
        self.qev1 = threading.Event()
        self.qev2 = threading.Event()
        self.desync_detect = False

        self.ptp_buffer = list()
        self.spoof_delay = 0.0005
        #### set up the GUI part
        self.gui = GUI(parent, self.queue)

        self.thread0 = PMUrun(1, '127.0.0.1', 1410, 2048, True)
        self.thread1 = PDCrun(1, '127.0.0.1', 1410, 2048, self.qev1, self.qLock1)
        self.thread2 = PMUrun(2, '127.0.0.1', 1420, 2048, True)
        self.thread3 = PDCrun(2, '127.0.0.1', 1420, 2048, self.qev2, self.qLock2)

        self.avgDelay1 = list()
        self.avgDelay2 = list()
        self.syncFactor = list()
        self.thread0.start()
        self.thread2.start()
        sleep(0.01)
        self.thread1.start()
        self.thread3.start()
        # anything
        self.periodicCall()

    def periodicCall(self):

        self.thread1.ts_buffer.clear()
        self.ptp_buffer.clear()

        ts1 = False
        ts2 = False

        try:
            self.ptpCapture()

            if self.qev1.isSet():
                self.qLock1.acquire()
                if len(self.thread1.ts_buffer) > 0:
                    tsbuff1 = self.thread1.ts_buffer.copy()
                    mesbuff1 = self.thread1.data_buffer.copy()
                    ts1 = True
                    self.thread1.ts_buffer.clear()
                    self.thread1.data_buffer.clear()
                self.qLock1.release()
                self.qev1.clear()

                if self.gui.spoof_status and ts1:
                    self.gpsspoof(tsbuff1, self.spoof_delay)
                    self.spoof_delay = self.spoof_delay + 0.1 * self.spoof_delay
                elif not self.gui.spoof_status:
                    self.spoof_delay = 0.001

            if self.qev2.isSet():
                self.qLock2.acquire()
                if len(self.thread3.ts_buffer) > 0:
                    tsbuff2 = self.thread3.ts_buffer.copy()
                    mesbuff2 = self.thread3.data_buffer.copy()
                    ts2 = True
                    self.thread3.ts_buffer.clear()
                    self.thread3.data_buffer.clear()
                self.qLock2.release()
                self.qev2.clear()

            if ts1 and ts2:
                self.calcandupdate(tsbuff1, mesbuff1, tsbuff2, mesbuff2)



        except UnboundLocalError or ValueError as e:
            print(e)
            self.parent.after(round((1000 * (1 / self.thread1.data_rate))), self.periodicCall)

        finally:
            if not self.running:
                # This is the brutal stop of the system. You may want to do
                # some cleanup before actually shutting it down.
                self.parent.quit()
                self.parent.destroy()
                import sys
                sys.exit(1)
            self.parent.after(round((1000 * (1 / self.thread1.data_rate))), self.periodicCall)
            # self.parent.after(5, self.periodicCall)

    def ptpCapture(self):
        for pak in cap.sniff_continuously(packet_count=1):
            self.ptp_buffer.append(p.assignPack(pak))

        cap.clear()

    def gpsspoof(self, tsbuff, delayfac):
        for dp in range(0, len(tsbuff)):
            tsbuff[dp] = tsbuff[dp] - delayfac  # add  delay

    def calcandupdate(self, tsbuff1, mesbuff1, tsbuff2, mesbuff2):
        tdelta = 0
        # print('PMU 1\n-------------------------')
        # print(' Length:', len(tsbuff1), ' Min:', min(tsbuff1), ' Max:', max(tsbuff1))
        # print(' Time Delta:', max(tsbuff1) - min(tsbuff1))
        # print('PMU 2\n-------------------------')
        # print(' Length:', len(tsbuff2), ' Min:', min(tsbuff2), ' Max:', max(tsbuff2))
        # print(' Time Delta:', max(tsbuff2) - min(tsbuff2))

        for i in range(0, len(tsbuff1)):
            tdelta = tdelta + (tsbuff2[i] - tsbuff1[i])
        tdelta = tdelta / len(tsbuff1)
        print(tdelta)
        self.syncFactor.append(tdelta)
        avgsynch = (sum(self.syncFactor)/len(self.syncFactor))
        print('Average time offset between PMUs:', avgsynch)
        # print('Time Differences- max:', max(tsbuff1) - max(tsbuff2), 'min:', min(tsbuff1) - min(tsbuff2))
        # print('-------------')

        # for pack in self.ptp_buffer:
        #     print(pack.mesType, '- time: ', pack.tsComplete)
        print(self.ptp_buffer[0].mesType, '- time: ', self.ptp_buffer[0].tsComplete)

        pmu_diff1 = self.ptp_buffer[0].tsComplete - min(tsbuff1)
        pmu_diff2 = self.ptp_buffer[0].tsComplete - min(tsbuff2)
        self.avgDelay1.append(pmu_diff1)
        self.avgDelay2.append(pmu_diff2)

        print('AVG PMU1-PTP Time Offset:', self.avgDelay1[len(self.avgDelay1) - 1])
        print('AVG PMU2-PTP Time Offset:', self.avgDelay2[len(self.avgDelay2) - 1])
        print('-------------\n')


        #### desync detection
        detect_threshold = 0.009
        if (tdelta > detect_threshold):
            self.desync_detect = True
        else:
            self.desync_detect = False


        #### update GUI with three data points: PMU level, PTP time, and PMU time
        pmu_scale = -10000
        if self.gui.cybergrid_status and not self.desync_detect:
            self.gui.update_GUI(self.desync_detect,
                            pmu_scale * tdelta,
                            pmu_scale * avgsynch,
                            datetime.utcfromtimestamp(self.ptp_buffer[0].tsComplete).strftime('%H:%M:%S.%f'),
                            datetime.utcfromtimestamp(max(tsbuff1)).strftime('%H:%M:%S.%f'),
                            datetime.utcfromtimestamp(max(tsbuff2)).strftime('%H:%M:%S.%f'))
        elif self.gui.cybergrid_status and self.desync_detect:
            self.gui.update_GUI(self.desync_detect,
                            pmu_scale * tdelta,
                            pmu_scale * avgsynch,
                            datetime.utcfromtimestamp(self.ptp_buffer[0].tsComplete).strftime('%H:%M:%S.%f'),
                            datetime.utcfromtimestamp(self.ptp_buffer[0].tsComplete).strftime('%H:%M:%S.%f'),
                            datetime.utcfromtimestamp(self.ptp_buffer[0].tsComplete).strftime('%H:%M:%S.%f'))
        elif not self.gui.cybergrid_status:
            self.gui.update_GUI(self.desync_detect,
                            pmu_scale * tdelta,
                            pmu_scale * avgsynch,
                            datetime.utcfromtimestamp(self.ptp_buffer[0].tsComplete).strftime('%H:%M:%S.%f'),
                            datetime.utcfromtimestamp(max(tsbuff1)).strftime('%H:%M:%S.%f'),
                            datetime.utcfromtimestamp(max(tsbuff2)).strftime('%H:%M:%S.%f'))


        self.running = self.gui.checkIfRunning()
        self.ptp_buffer.clear()
