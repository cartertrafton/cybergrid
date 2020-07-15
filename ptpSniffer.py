import pyshark
from time import sleep
from datetime import datetime


class ptpSniffer(object):

    def __init__(self, interface=None, capfile=None):
        self.interface = interface
        self.captureFile = capfile
        self.outPack = None
    def liveCapture(self, packcount = None, timeout = None, continuous = True):

        cap = pyshark.LiveCapture(interface=self.interface, display_filter='ptp')
        if not continuous:
            cap.sniff(packet_count=packcount, timeout=timeout)
            for pak in cap:
                outPack = self.assignPack(pak)
                outPack.printPackInfo()
                yield outPack

        elif continuous:
            for pak in cap.sniff_continuously():
                outPack = self.assignPack(pak)
                outPack.printPackInfo()
                self.outPack = outPack

    def fileCapture(self):
        cap = pyshark.FileCapture(self.captureFile, keep_packets=True, display_filter='ptp')
        global packData
        for pak in cap:
            outpack = self.assignPack(pak)
            yield outpack

    def assignPack(self, pak):

        if 'PTP' in pak:
            packData = ptpPacketData()
            ptpMessageType = int(pak.ptp.v2_control)
            if ptpMessageType == 5:
                packData = ptpPacketData(str(pak.ip.src), 'announce', int(pak.ptp.v2_sequenceId),
                                         int(pak.ptp.v2_an_origintimestamp_seconds),
                                         int(pak.ptp.v2_an_origintimestamp_nanoseconds),
                                         float(pak.ptp.v2_correction_ns))
                return packData

            if ptpMessageType == 0:
                packData = ptpPacketData(str(pak.ip.src), 'sync', int(pak.ptp.v2_sequenceId),
                                         int(pak.ptp.v2_sdr_origintimestamp_seconds),
                                         int(pak.ptp.v2_sdr_origintimestamp_nanoseconds),
                                         float(pak.ptp.v2_correction_ns))
                return packData

            if ptpMessageType == 2:
                packData = ptpPacketData(str(pak.ip.src), 'follow_up', int(pak.ptp.v2_sequenceId),
                                         int(pak.ptp.v2_fu_preciseorigintimestamp_seconds),
                                         int(pak.ptp.v2_fu_preciseorigintimestamp_nanoseconds),
                                         float(pak.ptp.v2_correction_ns))
                return packData
            if ptpMessageType == 1:
                packData = ptpPacketData(str(pak.ip.src), 'delay_request', int(pak.ptp.v2_sequenceId),
                                         int(pak.ptp.v2_sdr_origintimestamp_seconds),
                                         int(pak.ptp.v2_sdr_origintimestamp_nanoseconds),
                                         float(pak.ptp.v2_correction_ns))
                return packData
            if ptpMessageType == 3:
                packData = ptpPacketData(str(pak.ip.src), 'delay_response', int(pak.ptp.v2_sequenceId),
                                         int(pak.ptp.v2_dr_receivetimestamp_seconds),
                                         int(pak.ptp.v2_dr_receivetimestamp_nanoseconds),
                                         float(pak.ptp.v2_correction_ns))
                return packData

            # packData.printPackInfo()



class ptpPacketData(object):

    # Creates an object containing relevant PTP packet information
    def __init__(self, source=None, messageid=None, sequenceid=None, seconds_timestamp=None, seconds_nanoseconds=None, correction=None):
        self.sourceIP = source
        self.mesType = messageid
        self.s_timestamp = seconds_timestamp
        self.ns_timestamp = seconds_nanoseconds
        self.sequenceId = sequenceid
        self.correctionNs = correction
        if self.s_timestamp:
            self.tsComplete = float(str(self.s_timestamp)+'.'+str(self.ns_timestamp))
            self.timestampD_T = datetime.utcfromtimestamp(self.tsComplete).strftime('%Y-%m-%d %H:%M:%S')
        elif self.s_timestamp is None:
            self.tsComplete = float(str(0) + '.' + str(0))
            self.timestampD_T = datetime.utcfromtimestamp(self.tsComplete).strftime('%Y-%m-%d %H:%M:%S')


    def setData(self, source, messageid, sequenceid, seconds_timestamp, seconds_nanoseconds, correction):
        self.sourceIP = source
        self.mesType = messageid
        self.s_timestamp = seconds_timestamp
        self.ns_timestamp = seconds_nanoseconds
        self.sequenceId = sequenceid
        self.correctionNs = correction
        self.tsComplete = float(str(self.s_timestamp) + '.' + str(self.ns_timestamp))
        self.timestampD_T = datetime.utcfromtimestamp(self.tsComplete).strftime('%Y-%m-%d %H:%M:%S')

    def printPackInfo(self):
        print("Source:", self.sourceIP,
              "\nMessage type:", self.mesType,
              "\n\tSequence No:", self.sequenceId,
              "\n\tUnix Time (UTC):", self.tsComplete,
              "\n\tTimestamp (UTC):", self.timestampD_T)
