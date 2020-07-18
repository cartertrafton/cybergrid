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


if __name__ == "__main__":

    #### pre mainloop
    print("Starting CyberGrid...\n\n")
    welcome_cg()

    #### tkinter setup
    root = tk.Tk()
    root.title('CyberGrid')

    #### thread set up
    client = ThreadedClient(root)

    while client.running:
        try:

            root.update_idletasks()
            root.update()  # update the GUI

            #### GUI updating



        except:
            exit()


