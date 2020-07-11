import time
import pmuThreads
from threading import Thread
from ptpSniffer import ptpSniffer, ptpPacketData
from operator import sub
#
# class Cybernode(object):

# def findDiff(lista, listb):
#     C = list()
#     for i in range(0, len(lista)):
#         diff = listb[i]-lista[i]
#         C.append(diff)
#     return C

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



ptpCapture = ptpSniffer('enp3s0')

pmu1 = PMUrun(1, '127.0.0.1', 1410, 2048, True)
pmu2 = PMUrun(2, '127.0.0.1', 1420, 2048, True)
time.sleep(0.05)
pdc1 = PDCrun(1, '127.0.0.1', 1410, 2048)
pdc2 = PDCrun(2, '127.0.0.1', 1420, 2048)

fullSeq = [False, False, False, False]
pdc1TSBuffer = []
pdc1DataBuffer = []
pdc2TSBuffer = []
pdc2DataBuffer = []
tsDiff=[]
for pack in ptpCapture.liveCapture():

    if pack.mesType == 'Sync':
        fullSeq[1] = True
        syncPak = pack
    if pack.mesType == 'Announce':
        fullSeq[0] = True
        anncPak = pack
    if pack.mesType == 'Delay Request':
        fullSeq[2] = True
        delreqPak = pack
    if pack.mesType == 'Delay Response':
        fullSeq[3] = True
        delresPak = pack

    if fullSeq == [True, True, True, True]:
        anncPak.printPackInfo()
        syncPak.printPackInfo()
        delreqPak.printPackInfo()
        delresPak.printPackInfo()
        fullSeq = [False, False, False, False]


        if not (len(pdc1.ts_buffer) == 0 or len(pdc2.ts_buffer) == 0):
            pdc1TSBuffer = pdc1.ts_buffer
            pdc1DataBuffer = pdc1.data_buffer
            pdc2TSBuffer = pdc2.ts_buffer
            pdc2DataBuffer = pdc2.data_buffer
            tsDiff.append((max(pdc2TSBuffer) - min(pdc2TSBuffer))-(max(pdc1TSBuffer) - min(pdc1TSBuffer)))
            print('\nRunning average ts difference:', sum(tsDiff)/len(tsDiff),'\n')
            # print('delta t PMU 1:', max(pdc1TSBuffer) - min(pdc1TSBuffer),'delta t PMU 2:', max(pdc2TSBuffer) - min(pdc2TSBuffer))


        # print(len(pdc2TSBuffer),len(pdc1TSBuffer))
        pdc2.ts_buffer.clear()
        pdc2.data_buffer.clear()
        pdc1.ts_buffer.clear()
        pdc1.data_buffer.clear()

