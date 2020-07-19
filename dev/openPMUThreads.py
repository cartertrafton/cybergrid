import time
import pmuThreads
from threading import Thread
from ptpSniffer import ptpSniffer, ptpPacketData
import pyshark
import sys

from time import sleep

class PMUrun(Thread):
    def __init__(self, pmuid, pmuip, port, buffsize, setTS):

        self.pmu_id = pmuid
        self.pmu_ip = pmuip
        self.port = port
        self.buff_size = buffsize
        self.set_TS = setTS
        self.send = False
        self.ts_buffer = list()
        self.data_buffer = list()
        self.data_rate = pmuThreads.cybergridCfg.get_data_rate()
        Thread.__init__(self)
        self.daemon = True
        self.output = None

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
        self.data_rate = pmuThreads.cybergridCfg.get_data_rate()

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
                    dataOut.append(out)
                    seq += 1
                elif seq == self.data_rate:
                    self.send = True
                    self.ts_buffer = dataOut
                    dataOut.clear()
                    seq = 0


    def get_ts_buff(self):
        return self.ts_buffer

