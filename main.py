#
# cybergrid:
# microgrid security simulation software
#
# carter trafton & misha kharitonov
# wit 2020 - senior design
#
import tkinter as tk
import random
from gui.gui import *
# from openPMUThreads import *
from threading import Thread
from ptpSniffer import ptpSniffer, ptpPacketData
from threadedClient import *


def welcome_cg():
    print("Welcome to...")
    print("   _______     ______  ______ _____   _____ _____  _____ _____")
    print("  / ____\ \   / /  _ \|  ____|  __ \ / ____|  __ \|_   _|  __ \ ")
    print(" | |     \ \_/ /| |_) | |__  | |__) | |  __| |__) | | | | |  | |")
    print(" | |      \   / |  _ <|  __| |  _  /| | |_ |  _  /  | | | |  | |")
    print(" | |____   | |  | |_) | |____| | \ \| |__| | | \ \ _| |_| |__| |")
    print("  \_____|  |_|  |____/|______|_|  \_\\_____|_|  \_\_____|_____/ \n\n")
    return

# class cyberThread(Thread):
#     def __init__(self):
#         Thread.__init__(self)
#         self.daemon = True
#         self.start()
#
#     def run(self):
#         print("Starting Node\n")
#         startCybernode()



if __name__ == "__main__":

    #### pre mainloop
    print("Starting CyberGrid...\n\n")
    welcome_cg()

    #### tkinter setup
    root = tk.Tk()
    root.title('CyberGrid')

    #### thread set up
    client = ThreadedClient(root)

    #### creating GUI
    #gui = GUI(root)
    #gui.pack(side="top", fill="both", expand=True)
    #gui.update_GUI()
    #
    # ptpCapture = ptpSniffer('enp3s0', capfile='/home/cybergrid/cybergrid/ptpsample.pcap')
    #
    # pmu1 = PMUrun(1, '127.0.0.1', 1410, 2048, True)
    # pmu2 = PMUrun(2, '127.0.0.1', 1420, 2048, True)
    # time.sleep(0.05)
    # pdc1 = PDCrun(1, '127.0.0.1', 1410, 2048)
    # pdc2 = PDCrun(2, '127.0.0.1', 1420, 2048)
    #
    # fullSeq = [False, False, False, False]
    # pdc1TSBuffer = []
    # pdc1DataBuffer = []
    # pdc2TSBuffer = []
    # pdc2DataBuffer = []
    # tsDiff = []
    # p = ptpSniffer()
    # pack_list = []
    # cap = pyshark.LiveCapture(interface='enp3s0', display_filter='ptp')
    while client.running:
        try:

            root.update_idletasks()
            root.update()  # update the GUI

            #### GUI updating



        except:
            exit()


