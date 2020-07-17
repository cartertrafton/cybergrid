from openPMUThreads import *
import pmuThreads
import ptpSniffer
from time import sleep
import pyshark




ptpSeq = [ptpPacketData(), ptpPacketData(), ptpPacketData(), ptpPacketData(), ptpPacketData()]
# fullSeq = [False, False, False, False]
tsDiff = []
delay = None
ptpCapture = ptpSniffer('enp3s0',capfile='/home/cybergrid/cybergrid/ptpsample.pcap')
capture = pyshark.LiveCapture(interface='enp3s0', display_filter='ptp')
pmu1 = PMUrun(1, '127.0.0.1', 1410, 2048, True)
pmu2 = PMUrun(2, '127.0.0.1', 1420, 2048, True)
pdc1 = PDCrun(1, '127.0.0.1', 1410, 2048)
pdc2 = PDCrun(2, '127.0.0.1', 1420, 2048)

pmu1.start()
pmu2.start()
sleep(1/pdc2.data_rate)
pdc1.start()
pdc2.start()

while True:
    sleep(1)
    # for pak in capture.sniff_continuously(packet_count=5):
    #     packOut = ptpCapture.assignPack(pak)
    #     # packOut.printPackInfo()
    #     if packOut.mesType == 'sync':
    #         # fullSeq[0] = True
    #         ptpSeq[0] = packOut
    #     if packOut.mesType == 'follow_up':
    #         # fullSeq[1] = True
    #         ptpSeq[1] = packOut
    #     if packOut.mesType == 'delay_request':
    #         # fullSeq[2] = True
    #         ptpSeq[2] = packOut
    #     if packOut.mesType == 'delay_response':
    #         # fullSeq[3] = True
    #         ptpSeq[3] = packOut
    #     if packOut.mesType == 'announce':
    #         ptpSeq[4] = packOut
        # if fullSeq == [True, True, True, True]:
        #     break

        # delay = (folPak.tsComplete+delreqPak.tsComplete-syncPak.tsComplete-delresPak.tsComplete)/2
        # print('\n',delay,'\n')
        # fullSeq = [False, False, False, False]
    pdc1tsbuff = pdc1.get_ts_buff()
    pdc2tsbuff = pdc2.get_ts_buff()
    pdc1.ts_buffer.clear()
    pdc2.ts_buffer.clear()
    pdc2.data_buffer.clear()
    pdc1.data_buffer.clear()
    # for pack in ptpSeq:
    #     pack.printPackInfo()
    if (len(pdc1tsbuff) != 0) & (len(pdc2tsbuff) != 0):
        print(len(pdc2.ts_buffer))

        print(len(pdc1tsbuff))

        a1 = max(pdc1tsbuff)
        b1 = min(pdc1tsbuff)
        a2 = max(pdc2tsbuff)
        b2 = min(pdc2tsbuff)
        print(len(pdc1tsbuff), len(pdc2tsbuff))
        c = ptpSeq[0].tsComplete
        d = ptpSeq[3].tsComplete
        print('1: ',a1,b1,'2: ',a2,b2)
        tsDiff.append(((a1-b1)+(a2-b2)/2))
        print('\nRunning average ts difference:', sum(tsDiff)/len(tsDiff),'\n')

        print('delta t PMU 1:', max(a1) - min(b1),'delta t PMU 2:', max(a2) - min(b2))

rint('recieved: ', len(buff), 'time delta: ',max(buff)-min(buff))