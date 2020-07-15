import time
import threading
import queue
from gui.gui import *
from openPMUThreadsV2 import *
import pmuThreads
import pyshark

#
### adapted from
# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch09s07.html


### threadedClient class
class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """

    # this client launches GUI and worker thread
    def __init__(self, parent):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.parent = parent

        # Create the queue
        self.queue = queue.Queue()

        # Set up the GUI part
        self.gui = GUI(parent, self.queue)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        # self.thread1 = threading.Thread(target=self.workerThreads)
        # self.thread1.start()
        self.thread0 = PMUrun(1,'127.0.0.1',1410,2048, True, self.queue)
        self.thread1 = PDCrun(1,'127.0.0.1',1410, 2048, self.queue)
        self.thread2 = threading.Thread(target=self.ptp_worker, args={'interface': 'enp3s0', 'df' : 'ptp'})
        # Start the periodic call in the GUI to check if the queue contains
        self.thread0.start()
        sleep(0.001)
        self.thread1.start()
        self.thread2.start()
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """

        self.gui.update_GUI()
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.parent.after(1000, self.periodicCall)

    def ptp_worker(self, interface=None, df=None):
        cap = pyshark.LiveCapture(interface=interface, display_filter=df)
        while self.running:
            cap.sniff(timeout=1)
            for pak in cap:
                temp_pack = pak
                if 'PTP' in pak:
                    ptpMessageType = int(pak.ptp.v2_control)
                    if ptpMessageType == 5:
                        temp_pack = ptpPacketData(str(pak.ip.src), 'announce', int(pak.ptp.v2_sequenceId),
                                                  int(pak.ptp.v2_an_origintimestamp_seconds),
                                                  int(pak.ptp.v2_an_origintimestamp_nanoseconds),
                                                  float(pak.ptp.v2_correction_ns))
                    if ptpMessageType == 0:
                        temp_pack = ptpPacketData(str(pak.ip.src), 'sync', int(pak.ptp.v2_sequenceId),
                                                  int(pak.ptp.v2_sdr_origintimestamp_seconds),
                                                  int(pak.ptp.v2_sdr_origintimestamp_nanoseconds),
                                                  float(pak.ptp.v2_correction_ns))
                        self.queue.put(temp_pack)
                    if ptpMessageType == 2:
                        temp_pack = ptpPacketData(str(pak.ip.src), 'follow_up', int(pak.ptp.v2_sequenceId),
                                                  int(pak.ptp.v2_fu_preciseorigintimestamp_seconds),
                                                  int(pak.ptp.v2_fu_preciseorigintimestamp_nanoseconds),
                                                  float(pak.ptp.v2_correction_ns))
                        self.queue.put(temp_pack)
                    if ptpMessageType == 1:
                        temp_pack = ptpPacketData(str(pak.ip.src), 'delay_request', int(pak.ptp.v2_sequenceId),
                                                  int(pak.ptp.v2_sdr_origintimestamp_seconds),
                                                  int(pak.ptp.v2_sdr_origintimestamp_nanoseconds),
                                                  float(pak.ptp.v2_correction_ns))
                        self.queue.put(temp_pack)
                    if ptpMessageType == 3:
                        temp_pack = ptpPacketData(str(pak.ip.src), 'delay_response', int(pak.ptp.v2_sequenceId),
                                                  int(pak.ptp.v2_dr_receivetimestamp_seconds),
                                                  int(pak.ptp.v2_dr_receivetimestamp_nanoseconds),
                                                  float(pak.ptp.v2_correction_ns))
                        self.queue.put(temp_pack)

    def endApplication(self):
        self.running = 0
