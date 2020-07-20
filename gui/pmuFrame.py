import tkinter as tk
import random


class PmuDataDisplay(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # level set to random value for now
        self.canvas = tk.Canvas(self, background="white")
        self.canvas.pack(side="top", fill="both", expand=True)

        # create line for graph
        self.level_line1 = self.canvas.create_line(0, 0, 0, 0, fill="red")
        self.level_line2 = self.canvas.create_line(0, 0, 0, 0, fill="blue")


    def update_plot(self, lev1, lev2, spoof_status, cybergrid_status):
        # update the plot
        self.add_point(self.level_line1, lev1)
        self.add_point(self.level_line2, lev2)
        self.canvas.xview_moveto(1.0)
        return


    def add_point(self, line, y):
        coords = self.canvas.coords(line)
        x = coords[-2] + 10
        coords.append(x)
        coords.append(y)
        coords = coords[-800:]  # keep # of points to a manageable size
        self.canvas.coords(line, *coords)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        return
