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
        self.status1 = tk.Label(self.canvas, text="ACTIVE", bg='white', fg='blue', anchor='w', font=('consolas', 20))
        self.status2 = tk.Label(self.canvas, text="ACTIVE", bg='white', fg='blue', anchor='w', font=('consolas', 20))
        self.status1.place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.1)
        self.status2.place(relx=0.5, rely=0.5, relwidth=0.4, relheight=0.1)

    def update_status(self, status):
        # update the statuses
        if status:
            self.status1 = tk.Label(self.canvas, text="ACTIVE", bg='white', fg='blue', anchor='w', font=('consolas', 20))
            self.status2 = tk.Label(self.canvas, text="ACTIVE", bg='white', fg='blue', anchor='w', font=('consolas', 20))
        else:
            self.status1 = tk.Label(self.canvas, text="DISABLED", bg='white', fg='RED', anchor='w', font=('consolas', 20))
            self.status2 = tk.Label(self.canvas, text="DISABLED", bg='white', fg='RED', anchor='w', font=('consolas', 20))

        self.status1.place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.1)
        self.status2.place(relx=0.5, rely=0.5, relwidth=0.4, relheight=0.1)

        return
