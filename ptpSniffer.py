import pyshark

class ptpSniffer(object):

    def __init__(self, interface):
        self.interface = 'enp3s0'

    def capture(self):

        cap = pyshark.LiveCapture(interface=self.interface, display_filter='ptp')
        cap.sniff(packet_count=10)
        for pak in cap:
            if 'PTP' in pak:
                if hasattr(pak.ptp, 'v2_sdr_origintimestamp_seconds'):
                    print('sdr')
                    print(pak.ip.src, pak.ptp.v2_control, pak.ptp.v2_sdr_origintimestamp_seconds,
                          pak.ptp.v2_sdr_origintimestamp_nanoseconds)
                elif hasattr(pak.ptp, 'v2_an_origintimestamp_seconds'):
                    print('an')
                    print(pak.ip.src, pak.ptp.v2_control, pak.ptp.v2_an_origintimestamp_seconds,
                          pak.ptp.v2_an_origintimestamp_nanoseconds)
                else:
                    print('resp')
                    print(pak.ip.src, pak.ptp.v2_control, pak.ptp.v2_dr_receivetimestamp_seconds,
                          pak.ptp.v2_dr_receivetimestamp_nanoseconds)
class ptpError(BaseException):
    pass

class ptpPacketData(object):

    def __init__(self, source, messageid, seconds_timestamp, seconds_nanoseconds):
        self.source = source
        self.messageid == messageid
        self.s_timestamp = seconds_timestamp
        self.ns_timestamp = seconds_nanoseconds
