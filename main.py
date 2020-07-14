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

    while True:
        try:

            # for pack in ptpCapture.liveCapture():
            #
            #     if pack.mesType == 'Sync':
            #         fullSeq[1] = True
            #         syncPak = pack
            #     if pack.mesType == 'Announce':
            #         fullSeq[0] = True
            #         anncPak = pack
            #     if pack.mesType == 'Delay Request':
            #         fullSeq[2] = True
            #         delreqPak = pack
            #     if pack.mesType == 'Delay Response':
            #         fullSeq[3] = True
            #         delresPak = pack
            #     if fullSeq == [True, True, True, True]:
            #         break
            #
            # anncPak.printPackInfo()
            # syncPak.printPackInfo()
            # delreqPak.printPackInfo()
            # delresPak.printPackInfo()
            # fullSeq = [False, False, False, False]
            #
            # if not (len(pdc1.ts_buffer) == 0 or len(pdc2.ts_buffer) == 0):
            #     pdc1TSBuffer = pdc1.ts_buffer
            #     pdc1DataBuffer = pdc1.data_buffer
            #     pdc2TSBuffer = pdc2.ts_buffer
            #     pdc2DataBuffer = pdc2.data_buffer
            #     print(len(pdc1TSBuffer), len(pdc2TSBuffer))
            #     tsDiff.append((max(pdc2TSBuffer) - min(pdc2TSBuffer)) - (max(pdc1TSBuffer) - min(pdc1TSBuffer)))
            #     print('\nRunning average ts difference:', sum(tsDiff) / len(tsDiff), '\n')
            #     # print('delta t PMU 1:', max(pdc1TSBuffer) - min(pdc1TSBuffer),'delta t PMU 2:', max(pdc2TSBuffer) - min(pdc2TSBuffer))
            #
            # # print(len(pdc2TSBuffer),len(pdc1TSBuffer))
            # pdc2.ts_buffer.clear()
            # pdc2.data_buffer.clear()
            # pdc1.ts_buffer.clear()
            # pdc1.data_buffer.clear()

            #### GUI updating
            root.update_idletasks()
            root.update()  # update the GUI
            #gui.update_GUI()

        except:
            exit()


