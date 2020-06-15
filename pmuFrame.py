import tkinter as tk
import random


class pmuDataDisplay(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # level set to random value for now
        self.level = random.randint(0, 50)
        self.canvas = tk.Canvas(self, background="white")
        self.canvas.pack(side="top", fill="both", expand=True)

        # create line for graph
        self.level_line = self.canvas.create_line(0, 0, 0, 0, fill="red")
        self.update_plot()

    def update_plot(self):
        lev = random.randint(0, 200)
        self.add_point(self.level_line, lev)
        self.canvas.xview_moveto(1.0)
        self.after(100, self.update_plot)

    def add_point(self, line, y):
        coords = self.canvas.coords(line)
        x = coords[-2] + 1
        coords.append(x)
        coords.append(y)
        coords = coords[-800:]  # keep # of points to a manageable size
        self.canvas.coords(line, *coords)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

