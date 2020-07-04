import tkinter as tk
import random


class PmuDataDisplay(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # level set to random value for now
        self.level = random.randint(0, 50)
        self.canvas = tk.Canvas(self, background="white")
        self.canvas.pack(side="top", fill="both", expand=True)

        # create line for graph
        self.level_line = self.canvas.create_line(0, 0, 0, 0, fill="red")

    def update_plot(self, lev):
        # update the plot
        #print("updating pmu")
        self.add_point(self.level_line, lev)
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
