import pyshark
from time import sleep
from datetime import datetime


class ptpSniffer(object):

    def __init__(self, interface=None, capfile=None):
        self.interface = interface
        self.captureFile = capfile

    def liveCapture(self, packcount = None, continuous = True):

        cap = pyshark.LiveCapture(interface=self.interface, display_filter='ptp')
        global packData

        if not continuous:
            cap.sniff(packet_count=packcount)

            for pak in cap:
                if 'PTP' in pak:
                    ptpMessageType = int(pak.ptp.v2_control)
                    if ptpMessageType == 5:
                        packData = ptpPacketData(str(pak.ip.src), 'Announce', int(pak.ptp.v2_sequenceId),
                                                 int(pak.ptp.v2_an_origintimestamp_seconds),
                                                 int(pak.ptp.v2_an_origintimestamp_nanoseconds),
                                                 float(pak.ptp.v2_correction_ns))
                    if ptpMessageType == 0:
                        packData = ptpPacketData(str(pak.ip.src), 'Sync', int(pak.ptp.v2_sequenceId),
                                                 int(pak.ptp.v2_sdr_origintimestamp_seconds),
                                                 int(pak.ptp.v2_sdr_origintimestamp_nanoseconds),
                                                 float(pak.ptp.v2_correction_ns))
                    if ptpMessageType == 1:
                        packData = ptpPacketData(str(pak.ip.src), 'Delay Request', int(pak.ptp.v2_sequenceId),
                                                 int(pak.ptp.v2_sdr_origintimestamp_seconds),
                                                 int(pak.ptp.v2_sdr_origintimestamp_nanoseconds),
                                                 float(pak.ptp.v2_correction_ns))
                    if ptpMessageType == 3:
                        packData = ptpPacketData(str(pak.ip.src), 'Delay Response', int(pak.ptp.v2_sequenceId),
                                                 int(pak.ptp.v2_dr_receivetimestamp_seconds),
                                                 int(pak.ptp.v2_dr_receivetimestamp_nanoseconds),
                                                 float(pak.ptp.v2_correction_ns))

                #packData.printPackInfo()
                yield packData

        elif continuous:
            for pak in cap.sniff_continuously():
                if 'PTP' in pak:
                    ptpMessageType = int(pak.ptp.v2_control)
                    if ptpMessageType == 5:
                        packData = ptpPacketData(str(pak.ip.src), 'Announce', int(pak.ptp.v2_sequenceId),
                                                 int(pak.ptp.v2_an_origintimestamp_seconds),
                                                 int(pak.ptp.v2_an_origintimestamp_nanoseconds),
                                                 float(pak.ptp.v2_correction_ns))
                    if ptpMessageType == 0:
                        packData = ptpPacketData(str(pak.ip.src), 'Sync', int(pak.ptp.v2_sequenceId),
                                                 int(pak.ptp.v2_sdr_origintimestamp_seconds),
                                                 int(pak.ptp.v2_sdr_origintimestamp_nanoseconds),
                                                 float(pak.ptp.v2_correction_ns))
                    if ptpMessageType == 1:
                        packData = ptpPacketData(str(pak.ip.src), 'Delay Request', int(pak.ptp.v2_sequenceId),
                                                 int(pak.ptp.v2_sdr_origintimestamp_seconds),
                                                 int(pak.ptp.v2_sdr_origintimestamp_nanoseconds),
                                                 float(pak.ptp.v2_correction_ns))
                    if ptpMessageType == 3:
                        packData = ptpPacketData(str(pak.ip.src), 'Delay Response', int(pak.ptp.v2_sequenceId),
                                                 int(pak.ptp.v2_dr_receivetimestamp_seconds),
                                                 int(pak.ptp.v2_dr_receivetimestamp_nanoseconds),
                                                 float(pak.ptp.v2_correction_ns))

                    # packData.printPackInfo()
                    yield packData


    def fileCapture(self):
        cap = pyshark.FileCapture(self.captureFile, keep_packets=True, display_filter='ptp')
        global packData
        for pak in cap:
            if 'PTP' in pak:
                ptpMessageType = int(pak.ptp.v2_control)
                if ptpMessageType == 5:
                    packData = ptpPacketData(str(pak.ip.src), 'Announce', int(pak.ptp.v2_sequenceId),
                                             int(pak.ptp.v2_an_origintimestamp_seconds),
                                             int(pak.ptp.v2_an_origintimestamp_nanoseconds),
                                             float(pak.ptp.v2_correction_ns))
                if ptpMessageType == 0:
                    packData = ptpPacketData(str(pak.ip.src), 'Sync', int(pak.ptp.v2_sequenceId),
                                             int(pak.ptp.v2_sdr_origintimestamp_seconds),
                                             int(pak.ptp.v2_sdr_origintimestamp_nanoseconds),
                                             float(pak.ptp.v2_correction_ns))
                if ptpMessageType == 1:
                    packData = ptpPacketData(str(pak.ip.src), 'Delay Request', int(pak.ptp.v2_sequenceId),
                                             int(pak.ptp.v2_sdr_origintimestamp_seconds),
                                             int(pak.ptp.v2_sdr_origintimestamp_nanoseconds),
                                             float(pak.ptp.v2_correction_ns))
                if ptpMessageType == 3:
                    packData = ptpPacketData(str(pak.ip.src), 'Delay Response', int(pak.ptp.v2_sequenceId),
                                             int(pak.ptp.v2_dr_receivetimestamp_seconds),
                                             int(pak.ptp.v2_dr_receivetimestamp_nanoseconds),
                                             float(pak.ptp.v2_correction_ns))
                sleep(.5)
                # packData.printPackInfo()
                yield packData


class ptpPacketData(object):

    # Creates an object containing relevant PTP packet information
    def __init__(self, source, messageid, sequenceid, seconds_timestamp, seconds_nanoseconds, correction):
        self.sourceIP = source
        self.mesType = messageid
        self.s_timestamp = seconds_timestamp
        self.ns_timestamp = seconds_nanoseconds
        self.sequenceId = sequenceid
        self.correctionNs = correction
        self.tsComplete = float(str(self.s_timestamp)+'.'+str(self.ns_timestamp))
        self.timestampD_T = datetime.utcfromtimestamp(self.tsComplete).strftime('%Y-%m-%d %H:%M:%S')

    def printPackInfo(self):
        print("Source:", self.sourceIP,
              "\nMessage type:", self.mesType,
              "\n\tSequence No:", self.sequenceId,
              "\n\tUnix Time (UTC):", self.tsComplete,
              "\n\tTimestamp (UTC):", self.timestampD_T)
