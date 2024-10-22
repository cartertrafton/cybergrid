#
# cybergrid:
# microgrid security simulation software
#
# carter trafton & misha kharitonov
# wit 2020 - senior design
#
# gui.py
# This is the file for the GUI, built using python's tkinter library for creating GUIs
# Contains class for the GUI, and the functions for its control
#

import tkinter as tk
import random
import sys
import time
import threading
import queue
from gui.pmuFrame import PmuDataDisplay
from gui.mapFrame import SystemMapDisplay
from gui.nodeFrame import NodeDataDisplay

rand = random.Random()


#### GUI class
class GUI(tk.Frame):
    def __init__(self, parent, queue):
        tk.Frame.__init__(self)

        self.isRunning = 1

        #### queue
        self.queue = queue

        #### canvas and background
        self.canvas = tk.Canvas(parent, height=800, width=1600)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.background_label = tk.Label(parent, bg='gray')
        self.background_label.place(relwidth=1, relheight=1)

        #### status tracking variables
        self.spoof_status = False
        self.cybergrid_status = True
        self.change = False

        self.cybergrid_button = tk.StringVar()
        self.cybergrid_button.set("DEACTIVATE CYBERGRID")

        self.ptp_time = tk.StringVar()
        self.pmu_time1 = tk.StringVar()
        self.pmu_time2 = tk.StringVar()

        #### frames
        # node status frame
        self.node_frame = tk.Frame(parent, bg='white')
        self.node_frame.place(relx=0.025, rely=0.25, relwidth=0.45, relheight=0.30)
        # PMU data frame
        self.PMU_frame = tk.Frame(parent, bg='white', bd=5)
        self.PMU_frame.place(relx=0.525, rely=0.25, relwidth=0.45, relheight=0.30)
        # network map frame
        self.map_frame = tk.Frame(parent, bg='white', bd=5)
        self.map_frame.place(relx=0.025, rely=0.65, relwidth=0.45, relheight=0.30)
        # attack simulator frame
        self.attack_frame = tk.Frame(parent, bg='white', bd=5)
        self.attack_frame.place(relx=0.525, rely=0.65, relwidth=0.45, relheight=0.30)

        #### pack system map, PMU data, and node statuses into frames
        self.nodeDisplay = NodeDataDisplay(self.node_frame)
        self.nodeDisplay.pack(side="top", fill="both", expand=True)
        self.pmuDisplay = PmuDataDisplay(self.PMU_frame)
        self.pmuDisplay.pack(side="top", fill="both", expand=True)
        self.mapDisplay = SystemMapDisplay(self.map_frame)
        self.mapDisplay.pack(side="top", fill="both", expand=True)

        #### labels
        # frame labels
        self.label1 = tk.Label(parent, text="CONTROL CENTER", bg='gray', font=('consolas', 25))
        self.label1.place(relx=0.025, y=25, relwidth=0.3, relheight=0.1)
        self.label2 = tk.Label(parent, text="Nodes", bg='gray', anchor='w', font=('consolas', 20, 'underline'))
        self.label2.place(relx=0.025, rely=0.15, relwidth=0.5, relheight=0.1)
        self.label3 = tk.Label(parent, text="PMU", bg='gray', anchor='w', font=('consolas', 20, 'underline'))
        self.label3.place(relx=0.525, rely=0.15, relwidth=0.5, relheight=0.1)
        self.label4 = tk.Label(parent, text="Map", bg='gray', anchor='w', font=('consolas', 20, 'underline'))
        self.label4.place(relx=0.025, rely=0.55, relwidth=0.5, relheight=0.1)
        self.label5 = tk.Label(parent, text="Attack Simulator", bg='gray', anchor='w', font=('consolas', 20, 'underline'))
        self.label5.place(relx=0.525, rely=0.55, relwidth=0.5, relheight=0.1)


        #### buttons
        # reset
        self.button1 = tk.Button(parent, text="RESET", font=('consolas', 20), bg='white', fg='red', command=lambda: reset_sim(self))
        self.button1.place(relx=0.8, relwidth=0.1, relheight=0.1)
        # exit
        self.button2 = tk.Button(parent, text="EXIT", font=('consolas', 20), bg='white', fg='red', command=lambda: exit_sim(self))
        self.button2.place(relx=0.9, relwidth=0.1, relheight=0.1)
        # spoof
        self.button4 = tk.Button(self.attack_frame, text="SPOOF ATTACK", font=('consolas', 20), fg='red', command=lambda: spoof_attack(self))
        self.button4.place(relx=0.1, rely=0.2, relwidth=0.7, relheight=0.2)
        # cybergrid activate/deactivate
        self.button5 = tk.Button(self.attack_frame, textvariable=self.cybergrid_button, font=('consolas', 20), fg='red', command=lambda: disable_cybergrid(self))
        self.button5.place(relx=0.1, rely=0.5, relwidth=0.7, relheight=0.2)

    def update_GUI(self, desync_detect, pmu_level1, pmu_level2, ptp_t, pmu_t1, pmu_t2):
        #### set time variables
        self.ptp_time.set(ptp_t)
        self.pmu_time1.set(pmu_t1)
        self.pmu_time2.set(pmu_t2)

        #### update PMU display
        self.pmuDisplay.update_plot(pmu_level1, pmu_level2, not self.spoof_status, self.cybergrid_status)

        #### update Node time
        self.nodeDisplay.update_time(self.ptp_time, self.pmu_time1, self.pmu_time2)

        #### update system map, if change has been made
        if self.change:
            self.nodeDisplay.update_ptp_status(self.cybergrid_status)
            self.mapDisplay.update_map(not self.spoof_status, self.cybergrid_status)
            self.change = False

        self.nodeDisplay.update_pmu_status(desync_detect, self.cybergrid_status)

        return


    def checkIfRunning(self):
        return self.isRunning


#### functions
# reset program
def reset_sim(self):
    self.spoof_status = False
    self.cybergrid_status = True
    self.change = True
    self.cybergrid_button.set("DEACTIVATE CYBERGRID")
    return


# exit program
def exit_sim(self):
    print("Exiting CyberGrid...")
    self.isRunning = 0
    return


# spoof attack
def spoof_attack(self):
    #print("switching GPS sources...")
    self.spoof_status = not self.spoof_status
    self.change = True
    return


# cybergrid activate/deactivate
def disable_cybergrid(self):
    self.cybergrid_status = not self.cybergrid_status
    self.change = True
    if self.cybergrid_status == True:
        self.cybergrid_button.set("DEACTIVATE CYBERGRID")
    else:
        self.cybergrid_button.set("ACTIVATE CYBERGRID")
    return

