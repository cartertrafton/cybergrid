import tkinter as tk
import random


class systemMapDisplay(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.canvas = tk.Canvas(self, background="white")
        self.canvas.pack(side="top", fill="both", expand=True)


        # node connections
        self.node1_connection = self.canvas.create_line(150, 75, 350, 75, fill="blue", width=10)
        self.node2_connection = self.canvas.create_line(150, 135, 350, 135, fill="blue", width=10)
        # PMU connections
        self.PMU_CC_connection = self.canvas.create_line(350, 200, 350, 75, fill="GREEN", width=10)
        self.PMU_node_connection1 = self.canvas.create_line(125, 150, 125, 185, fill="GREEN", width=10)
        self.PMU_node_connection2 = self.canvas.create_line(120, 185, 300, 185, fill="GREEN", width=10)
        # GPS connection line
        self.GPS_connection = self.canvas.create_line(50, 150, 175, 150, fill="BLACK", width=10)
        # Attack connection line
        self.Attack_connection = self.canvas.create_line(50, 200, 300, 200, fill="RED", width=10)


        # create map nodes & labels
        self.node2 = self.canvas.create_rectangle(100, 50, 250, 100, fill="white")
        self.node2_label = self.canvas.create_text(150, 75, text="Node 2")
        self.node1 = self.canvas.create_rectangle(100, 110, 250, 160, fill="white")
        self.node1_label = self.canvas.create_text(150, 135, text="Node 1")
        self.Control_center_node = self.canvas.create_rectangle(300, 50, 450, 150, fill="white")
        self.Control_center_node_label = self.canvas.create_text(375, 100, text="Control Center")
        self.PMU_node = self.canvas.create_rectangle(200, 175, 400, 225, fill="white")
        self.PMU_node_label = self.canvas.create_text(300, 200, text="PMU")

        self.gps_label = self.canvas.create_text(30, 140, text="GPS")
        self.attack_label = self.canvas.create_text(30, 180, text="ATTACK")

        self.update_map()

    def update_map(self):
        # check node status 1
        # update
        # check node status 2
        # update
        # check PMU verification
        # update
        print("test")
        return

