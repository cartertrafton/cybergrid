#
# cybergrid:
# microgrid security simulation software
#
# carter trafton & misha kharitonov
# wit 2020 - senior design
#

import tkinter as tk
from pmuFrame import pmuDataDisplay

HEIGHT = 800
WIDTH = 1200


#### functions
# reset program
def reset_sim():
    # just for testing now
    print("reset activated")


# exit program
def exit_sim():
    print("Exiting CyberGrid...")
    root.quit()
    root.destroy()


# switch power source
def switch_power_source():
    print("switching power sources...")


# switch GPS source
def switch_gps_source():
    print("switching GPS sources...")


# cybergrid activate/deactivate
def disable_cybergrid():
    print("CYBERGRID!!!!")


#### tkinter setup
root = tk.Tk()
root.title('CyberGrid')

#### canvas and background
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()
background_label = tk.Label(root, bg='gray')
background_label.place(relwidth=1, relheight=1)

#### frames
# node status frame
node_frame = tk.Frame(root, bg='white')
node_frame.place(relx=0.025, rely=0.15, relwidth=0.45, relheight=0.35)
# PMU data frame
PMU_frame = tk.Frame(root, bg='white', bd=5)
PMU_frame.place(relx=0.525, rely=0.15, relwidth=0.45, relheight=0.35)
# network map frame
map_frame = tk.Frame(root, bg='white', bd=5)
map_frame.place(relx=0.025, rely=0.55, relwidth=0.45, relheight=0.35)
# attack simulator frame
attack_frame = tk.Frame(root, bg='white', bd=5)
attack_frame.place(relx=0.525, rely=0.55, relwidth=0.45, relheight=0.35)

#### labels
# frame labels
label1 = tk.Label(root, text="CONTROL CENTER", bg='gray', font=('consolas', 25))
label1.place(relx=0.025, y=25, relwidth=0.3, relheight=0.1)
label2 = tk.Label(node_frame, text="Nodes", bg='white', anchor='w', font=('consolas', 20, 'underline'))
label2.place(x=25, rely=0.05, relwidth=0.5, relheight=0.1)
label3 = tk.Label(PMU_frame, text="PMU", bg='white', anchor='w', font=('consolas', 20, 'underline'))
label3.place(x=25, rely=0.05, relwidth=0.5, relheight=0.1)
label4 = tk.Label(map_frame, text="Map", bg='white', anchor='w', font=('consolas', 20, 'underline'))
label4.place(x=25, rely=0.05, relwidth=0.5, relheight=0.1)
label5 = tk.Label(attack_frame, text="Attack Simulator", bg='white', anchor='w', font=('consolas', 20, 'underline'))
label5.place(x=25, rely=0.05, relwidth=0.5, relheight=0.1)

# node status & time labels
label6 = tk.Label(node_frame, text="1: STATUS: ", bg='white', font=('consolas', 20))
label6.place(relx=0.025, rely=0.2, relwidth=0.5, relheight=0.1)
label7 = tk.Label(node_frame, text="   TIME: ", bg='white', font=('consolas', 20))
label7.place(relx=0.025, rely=0.4, relwidth=0.5, relheight=0.1)
label8 = tk.Label(node_frame, text="2: STATUS: ", bg='white', font=('consolas', 20))
label8.place(relx=0.025, rely=0.6, relwidth=0.5, relheight=0.1)
label9 = tk.Label(node_frame, text="   TIME: ", bg='white', font=('consolas', 20))
label9.place(relx=0.025, rely=0.8, relwidth=0.5, relheight=0.1)

#### buttons
# reset
button1 = tk.Button(root, text="RESET", font=('consolas', 20), bg='white', fg='red', command=reset_sim)
button1.place(relx=0.8, relwidth=0.1, relheight=0.1)
# exit
button2 = tk.Button(root, text="EXIT", font=('consolas', 20), bg='white', fg='red', command=exit_sim)
button2.place(relx=0.9, relwidth=0.1, relheight=0.1)
# power source
button3 = tk.Button(attack_frame, text="POWER SPOOF", font=('consolas', 20), fg='red', command=switch_power_source)
button3.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.2)
# gps source
button4 = tk.Button(attack_frame, text="GPS SPOOF", font=('consolas', 20), fg='red', command=switch_gps_source)
button4.place(relx=0.2, rely=0.5, relwidth=0.6, relheight=0.2)
# cybergrid activate/deactivate
button5 = tk.Button(attack_frame, text="DISABLE CYBERGRID", font=('consolas', 20), fg='red', command=disable_cybergrid)
button5.place(relx=0.2, rely=0.8, relwidth=0.6, relheight=0.2)

#### pre mainloop
print("Starting CyberGrid...")

pmuDataDisplay(PMU_frame).pack(side="top", fill="both", expand=True)
systemMapDisplay(map_frame).pack(side="top", fill="both", expand=True)

# cybergrid sim begin


#### main tkinter loop
# root.mainloop()			# scrapped until can understand mainloop
while True:
    # get data and update node statuses

    try:
        root.update_idletasks()
        root.update()  # update the GUI
    except:
        exit()
