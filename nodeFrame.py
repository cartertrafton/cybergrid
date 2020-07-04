import tkinter as tk


class NodeDataDisplay(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.canvas = tk.Canvas(self, background="white")
        self.canvas.pack(side="top", fill="both", expand=True)

        # node status & time labels
        self.status_label1 = tk.Label(self.canvas, text="1: STATUS: ", bg='white', font=('consolas', 20))
        self.status_label1.place(relx=0.025, rely=0.1, relwidth=0.5, relheight=0.1)
        self.time_label1 = tk.Label(self.canvas, text="   TIME: ", bg='white', font=('consolas', 20))
        self.time_label1.place(relx=0.025, rely=0.3, relwidth=0.5, relheight=0.1)
        self.status_label2 = tk.Label(self.canvas, text="2: STATUS: ", bg='white', font=('consolas', 20))
        self.status_label2.place(relx=0.025, rely=0.5, relwidth=0.5, relheight=0.1)
        self.time_label2 = tk.Label(self.canvas, text="   TIME: ", bg='white', font=('consolas', 20))
        self.time_label2.place(relx=0.025, rely=0.7, relwidth=0.5, relheight=0.1)


        # create line for graph
        self.update_status()

    def update_status(self):
        # update the plot
        #print("updating nodes")
        temp = 0
        return

