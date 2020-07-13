import time
import pmuThreads
from threading import Thread
from ptpSniffer import ptpSniffer, ptpPacketData
from operator import sub
#
# class Cybernode(object):
from time import sleep

class PMUrun(Thread):
    def __init__(self, pmuid, pmuip, port, buffsize, setTS):
        self.pmu_id = pmuid
        self.pmu_ip = pmuip
        self.port = port
        self.buff_size = buffsize
        self.set_TS = setTS

        Thread.__init__(self)
        self.daemon = True
        self.output = None
        self.start()

    def run(self):
        print("Starting PMU "+str(self.pmu_id)+"\n")
        pmuThreads.pmuThread(self.pmu_id, self.pmu_ip, self.port, self.buff_size, self.set_TS)


class PDCrun(Thread):

    def __init__(self, pdcid, pdcip, port, buffsize):
        self.pdc_id = pdcid
        self.pdc_ip = pdcip
        self.port = port
        self.buff_size = buffsize
        self.ts_buffer = list()
        self.data_buffer = list()
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        print("Starting PDC "+str(self.pdc_id)+"\n")
        while True:
            for out in pmuThreads.pdcThread(self.pdc_id, self.pdc_ip, self.port, self.buff_size):
                self.ts_buffer.append(out['time'])
                self.data_buffer.append((out['measurements']))
                # print(out)

    def get_ts_buff(self):
        return self.ts_buffer




fullSeq = [False, False, False, False]

tsDiff = []
delay = None
ptpCapture = ptpSniffer('enp3s0',capfile='/home/cybergrid/cybergrid/ptpsample.pcap')
pmu1 = PMUrun(1, '127.0.0.1', 1410, 2048, True)
pmu2 = PMUrun(2, '127.0.0.1', 1420, 2048, True)
sleep(0.01)
pdc1 = PDCrun(1, '127.0.0.1', 1410, 2048)
pdc2 = PDCrun(2, '127.0.0.1', 1420, 2048)
for pack in ptpCapture.liveCapture():
    if pack.mesType == 'sync':
        fullSeq[0] = True
        syncPak = pack
    if pack.mesType == 'follow_up':
        fullSeq[1] = True
        folPak = pack
    if pack.mesType == 'delay_request':
        fullSeq[2] = True
        delreqPak = pack
    if pack.mesType == 'delay_response':
        fullSeq[3] = True
        delresPak = pack

    if fullSeq == [True, True, True, True]:
        syncPak.printPackInfo()
        folPak.printPackInfo()
        delreqPak.printPackInfo()
        delresPak.printPackInfo()
        delay = (folPak.tsComplete+delreqPak.tsComplete-syncPak.tsComplete-delresPak.tsComplete)/2
        print('\n',delay,'\n')

        if (len(pdc1.ts_buffer) != 0) & (len(pdc2.ts_buffer) != 0):
            print(len(pdc2.ts_buffer))

            print(len(pdc1.ts_buffer))

            a1 = max(pdc1.ts_buffer)
            b1 = min(pdc1.ts_buffer)
            a2 = max(pdc2.ts_buffer)
            b2 = min(pdc2.ts_buffer)
            c = delresPak.tsComplete
            d = syncPak.tsComplete
            print('1: ',a1,b1,'2: ',a2,b2)
            tsDiff.append(((a1-b1)+(a2-b2)/2))
            print('\nRunning average ts difference:', sum(tsDiff)/len(tsDiff),'\n')

            # print('delta t PMU 1:', max(pdc1TSBuffer) - min(pdc1TSBuffer),'delta t PMU 2:', max(pdc2TSBuffer) - min(pdc2TSBuffer))

        fullSeq = [False, False, False, False]

        # print(len(pdc2TSBuffer),len(pdc1TSBuffer))
        pdc2.ts_buffer.clear()
        pdc2.data_buffer.clear()
        pdc1.ts_buffer.clear()
        pdc1.data_buffer.clear()

