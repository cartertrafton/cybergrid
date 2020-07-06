import pyshark
import time
from datetime import datetime


class ptpSniffer(object):

    def __init__(self, interface):
        self.interface = 'enp3s0'

    def capture(self, packCount):

        global packData
        cap = pyshark.LiveCapture(interface=self.interface, display_filter='ptp')
        cap.sniff(packet_count=packCount)

        for pak in cap:
            if 'PTP' in pak:
                ptpMessageType = int(pak.ptp.v2_control)
                if ptpMessageType == 5:
                    packData = ptpPacketData(str(pak.ip.src), 'Announce', int(pak.ptp.v2_sequenceId),
                                  int(pak.ptp.v2_an_origintimestamp_seconds),
                                  int(pak.ptp.v2_an_origintimestamp_nanoseconds), float(pak.ptp.v2_correction_ns))
                if ptpMessageType== 0:
                    packData = ptpPacketData(str(pak.ip.src), 'Sync', int(pak.ptp.v2_sequenceId),
                                  int(pak.ptp.v2_sdr_origintimestamp_seconds),
                                  int(pak.ptp.v2_sdr_origintimestamp_nanoseconds), float(pak.ptp.v2_correction_ns))
                if ptpMessageType == 1:
                    packData = ptpPacketData(str(pak.ip.src), 'Delay Request', int(pak.ptp.v2_sequenceId),
                                  int(pak.ptp.v2_sdr_origintimestamp_seconds),
                                  int(pak.ptp.v2_sdr_origintimestamp_nanoseconds), float(pak.ptp.v2_correction_ns))
                if ptpMessageType == 3:
                    packData = ptpPacketData(str(pak.ip.src), 'Delay Response', int(pak.ptp.v2_sequenceId),
                                  int(pak.ptp.v2_dr_receivetimestamp_seconds),
                                  int(pak.ptp.v2_dr_receivetimestamp_nanoseconds), float(pak.ptp.v2_correction_ns))

                packData.printPackInfo()

#
# class ptpError(BaseException):
#     pass


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
