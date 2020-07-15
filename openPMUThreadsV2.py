import time
import pmuThreads
from threading import Thread
from ptpSniffer import ptpSniffer, ptpPacketData
import pyshark
import queue
#
# class Cybernode(object):
from time import sleep
import nest_asyncio

nest_asyncio.apply()


class PMUrun(Thread):
    def __init__(self, pmuid, pmuip, port, buffsize, setTS, queue):
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

    def __init__(self, pdcid, pdcip, port, buffsize, queue):
        self.pdc_id = pdcid
        self.pdc_ip = pdcip
        self.port = port
        self.buff_size = buffsize
        self.ts_buffer = list()
        self.data_buffer = list()
        self.queue = queue
        Thread.__init__(self)
        self.daemon = True
        self.data_rate = pmuThreads.cybergridCfg.get_data_rate()

    def run(self):
        print("Starting PDC " + str(self.pdc_id) + "\n")
        while self.isAlive():
            for out in pmuThreads.pdcThread(self.pdc_id, self.pdc_ip, self.port, self.buff_size):
                if len(self.ts_buffer)<self.data_rate:
                    self.ts_buffer.append(out['time'])
                    if len(self.ts_buffer)==self.data_rate:
                        print('---',len(self.ts_buffer))
                        self.queue.put(self.ts_buffer)
                        self.ts_buffer.clear()
                # print(out)

    def get_ts_buff(self):
        return self.ts_buffer


class ptpThread(Thread):

    def __init__(self, interface, dispfilter, queue):
        self.interface = interface
        self.disp_filter = dispfilter
        self.pack_list = []
        self.queue = queue
        Thread.__init__(self)
        self.daemon = True
        # self.start()

    def run(self):
        cap = pyshark.LiveCapture(interface=self.interface, display_filter=self.disp_filter)
        p = ptpSniffer()
        while True:
            for pak in cap.sniff_continuously(packet_count=5):
                ob = p.assignPack(pak)
                self.pack_list.append(ob)
                if len(self.pack_list) == 5:
                    self.queue.put(self.pack_list)
                    self.pack_list.clear()
                    break


#
# tsDiff = []
# delay = None
ptpCapture = ptpSniffer(interface='enp3s0', capfile='/home/cybergrid/cybergrid/ptpsample.pcap')
ptpCapture.liveCapture()
# pmu1 = PMUrun(1, '127.0.0.1', 1410, 2048, True)
# pmu2 = PMUrun(2, '127.0.0.1', 1420, 2048, True)
# sleep(0.01)
# pdc1 = PDCrun(1, '127.0.0.1', 1410, 2048)
# pdc2 = PDCrun(2, '127.0.0.1', 1420, 2048)
# ptp = ptpThread('enp3s0', 'ptp')
#
# ptp.start()
# pmu1.start()
# pmu2.start()
# pdc1.start()
# pdc2.start()
#
# for thread in [ptp, pmu1, pdc1, pmu2, pdc2]:
#     thread.start()
#     thread.join()
#
# while True:
#     # while len(pdc1.ts_buffer) < 60 & len(pdc2.ts_buffer) < 60:
#     #     pass
#     # pass
#     this_pack = ptp.pack_cap
#     this_pack[0].printPackInfo()
#     if (len(pdc1.ts_buffer) >= 60) and (len(pdc2.ts_buffer) >= 60):
#         print(len(pdc2.ts_buffer))
#         print(len(pdc1.ts_buffer))
#
#         a1 = max(pdc1.ts_buffer)
#         b1 = min(pdc1.ts_buffer)
#         a2 = max(pdc2.ts_buffer)
#         b2 = min(pdc2.ts_buffer)
#         # c = delresPak.tsComplete
#         # d = syncPak.tsComplete
#         print('1 (min, max):', b1, a1, '\n2 (min, max):', b2, a2)
#         # tsDiff.append((a1 - b1) - (a2 - b2))
#         # print('\nRunning average ts difference:', sum(tsDiff) / len(tsDiff), '\n')
#
#         print('delta t PMU 1:', max(pdc1.ts_buffer) - min(pdc1.ts_buffer), 'delta t PMU 2:',
#               max(pdc2.ts_buffer) - min(pdc2.ts_buffer))
#         print('Difference of Delta T between 1 and 2:    ', (a1 - b1) - (a2 - b2))
#         # capture.sniff(packet_count=1)
# for pak in capture:
#     if 'PTP' in pak:
#         ptpMessageType = int(pak.ptp.v2_control)
#         if ptpMessageType == 5:
#             packData = ptpPacketData(str(pak.ip.src), 'announce', int(pak.ptp.v2_sequenceId),
#                                      int(pak.ptp.v2_an_origintimestamp_seconds),
#                                      int(pak.ptp.v2_an_origintimestamp_nanoseconds),
#                                      float(pak.ptp.v2_correction_ns))
#         if ptpMessageType == 0:
#             packData = ptpPacketData(str(pak.ip.src), 'sync', int(pak.ptp.v2_sequenceId),
#                                      int(pak.ptp.v2_sdr_origintimestamp_seconds),
#                                      int(pak.ptp.v2_sdr_origintimestamp_nanoseconds),
#                                      float(pak.ptp.v2_correction_ns))
#         if ptpMessageType == 2:
#             packData = ptpPacketData(str(pak.ip.src), 'follow_up', int(pak.ptp.v2_sequenceId),
#                                      int(pak.ptp.v2_fu_preciseorigintimestamp_seconds),
#                                      int(pak.ptp.v2_fu_preciseorigintimestamp_nanoseconds),
#                                      float(pak.ptp.v2_correction_ns))
#         if ptpMessageType == 1:
#             packData = ptpPacketData(str(pak.ip.src), 'delay_request', int(pak.ptp.v2_sequenceId),
#                                      int(pak.ptp.v2_sdr_origintimestamp_seconds),
#                                      int(pak.ptp.v2_sdr_origintimestamp_nanoseconds),
#                                      float(pak.ptp.v2_correction_ns))
#         if ptpMessageType == 3:
#             packData = ptpPacketData(str(pak.ip.src), 'delay_response', int(pak.ptp.v2_sequenceId),
#                                      int(pak.ptp.v2_dr_receivetimestamp_seconds),
#                                      int(pak.ptp.v2_dr_receivetimestamp_nanoseconds),
#                                      float(pak.ptp.v2_correction_ns))
# packData.printPackInfo()
# pdc2.ts_buffer.clear()
# pdc2.data_buffer.clear()
# pdc1.ts_buffer.clear()
# pdc1.data_buffer.clear()
