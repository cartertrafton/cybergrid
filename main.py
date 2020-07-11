#
# cybergrid:
# microgrid security simulation software
#
# carter trafton & misha kharitonov
# wit 2020 - senior design
#
import tkinter as tk
import random
from gui.gui import GUI
from openPMUThreads import *
from threading import Thread

def welcome_cg():
    print("Welcome to...")
    print("   _______     ______  ______ _____   _____ _____  _____ _____")
    print("  / ____\ \   / /  _ \|  ____|  __ \ / ____|  __ \|_   _|  __ \ ")
    print(" | |     \ \_/ /| |_) | |__  | |__) | |  __| |__) | | | | |  | |")
    print(" | |      \   / |  _ <|  __| |  _  /| | |_ |  _  /  | | | |  | |")
    print(" | |____   | |  | |_) | |____| | \ \| |__| | | \ \ _| |_| |__| |")
    print("  \_____|  |_|  |____/|______|_|  \_\\_____|_|  \_\_____|_____/ \n\n")
    return

class cyberThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        print("Starting Node\n")
        startCybernode()



if __name__ == "__main__":

    #### pre mainloop
    print("Starting CyberGrid...\n\n")
    welcome_cg()

    #### tkinter setup
    root = tk.Tk()
    root.title('CyberGrid')

    #### creating GUI
    gui = GUI(root)
    gui.pack(side="top", fill="both", expand=True)
    gui.update_GUI()

    cn1 = cyberThread()
    while True:
        try:
            #### GUI updating
            root.update_idletasks()
            root.update()  # update the GUI
            gui.update_GUI()

        except:
            exit()


