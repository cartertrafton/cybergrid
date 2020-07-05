import pyshark
import time

class ptpSniffer(object):

    def __init__(self, interface):
        self.interface = 'enp3s0'

    def capture(self):

        cap = pyshark.LiveCapture(interface=self.interface, display_filter='ptp')
        cap.sniff(packet_count=1)
        for pak in cap:
            if 'PTP' in pak:
                # if hasattr(pak.ptp.v2_control == 5):

                if hasattr(pak.ptp, 'v2_an_origintimestamp_seconds'):
                    print('an')
                    print(pak.ip.src, pak.ptp.v2_control, pak.ptp.v2_an_origintimestamp_seconds,
                          pak.ptp.v2_an_origintimestamp_nanoseconds)
                else:
                    print('resp')
                    # print(pak.ip.src, pak.ptp.v2_control, pak.ptp.v2_dr_receivetimestamp_seconds,
                    #       pak.ptp.v2_dr_receivetimestamp_nanoseconds)
class ptpError(BaseException):
    pass

class ptpPacketData(object):
            #Creates an object containing relevant PTP packet information
    def __init__(self, source, messageid, sequenceId, seconds_timestamp, seconds_nanoseconds, correction):
        self.source = source
        self.msgType == messageid
        self.s_timestamp = seconds_timestamp
        self.ns_timestamp = seconds_nanoseconds
        self.sequenceId = sequenceId
        self.correctionNs = correction
        self.timestampD_T = ''
        self.tsComplete = 0
    def getTimestamp(self):
        completeTS = self.s_timestamp + self.ns_timestamp
        dateTime = time.time()