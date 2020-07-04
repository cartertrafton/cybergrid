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
from pmuFrame import PmuDataDisplay
from mapFrame import SystemMapDisplay
from nodeFrame import NodeDataDisplay


#### GUI class
class GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self)

        #### canvas and background
        self.canvas = tk.Canvas(parent, height=800, width=1200)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.background_label = tk.Label(parent, bg='gray')
        self.background_label.place(relwidth=1, relheight=1)

        #### status tracking variables
        self.gps_status = True
        self.power_status = True
        self.cybergrid_status = True
        self.change = False

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
        self.button2 = tk.Button(parent, text="EXIT", font=('consolas', 20), bg='white', fg='red', command=lambda: exit_sim(parent))
        self.button2.place(relx=0.9, relwidth=0.1, relheight=0.1)
        # power source
        self.button3 = tk.Button(self.attack_frame, text="POWER SPOOF", font=('consolas', 20), fg='red', command=lambda: switch_power_source(self))
        self.button3.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.2)
        # gps source
        self.button4 = tk.Button(self.attack_frame, text="GPS SPOOF", font=('consolas', 20), fg='red', command=lambda: switch_gps_source(self))
        self.button4.place(relx=0.2, rely=0.4, relwidth=0.6, relheight=0.2)
        # cybergrid activate/deactivate
        self.button5 = tk.Button(self.attack_frame, text="DISABLE CYBERGRID", font=('consolas', 20), fg='red', command=lambda: disable_cybergrid(self))
        self.button5.place(relx=0.2, rely=0.7, relwidth=0.6, relheight=0.2)

    def update_GUI(self):
        self.pmuDisplay.update_plot(random.randint(0, 200))
        if self.change:
            self.nodeDisplay.update_status(self.cybergrid_status)
            self.mapDisplay.update_map(self.gps_status, self.power_status, self.cybergrid_status)
            self.change = False

        return


#### functions
# reset program
def reset_sim(self):
    self.gps_status = True
    self.power_status = True
    self.cybergrid_status = True
    return


# exit program
def exit_sim(parent):
    print("Exiting CyberGrid...")
    parent.quit()
    parent.destroy()
    return


# switch power source
def switch_power_source(self):
    self.power_status = not self.power_status
    self.change = True
    return


# switch GPS source
def switch_gps_source(self):
    #print("switching GPS sources...")
    self.gps_status = not self.gps_status
    self.change = True
    return


# cybergrid activate/deactivate
def disable_cybergrid(self):
    self.cybergrid_status = not self.cybergrid_status
    self.change = True
    return

