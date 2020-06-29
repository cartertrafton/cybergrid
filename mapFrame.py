import tkinter as tk
import random


class systemMapDisplay(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.canvas = tk.Canvas(self, background="white")
        self.canvas.pack(side="top", fill="both", expand=True)

        # create map nodes
        self.node1 = ""
        self.node2 = ""
        self.PMU_node = ""
        self.Control_center_node = ""

        # create connection lines for map
        self.node1_connection = self.canvas.create_line(0, 0, 100, 100, fill="GREEN")
        self.node2_connection = self.canvas.create_line(0, 0, 100, 100, fill="GREEN")
        self.PMU_connection = self.canvas.create_line

        self.update_map()

    def update_map(self):
        # check node status 1
        # check node status 2
        # check PMU verification




