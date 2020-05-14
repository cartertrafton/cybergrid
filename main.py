#
# cybergrid:
# microgrid security simulation software
#
# carter trafton & misha kharitonov
# wit 2020 - senior design
#

import tkinter as tk

HEIGHT = 600
WIDTH = 800


#### functions
# reset program
def reset_sim():
    # just for testing now
    print("reset activated")


# exit program
def exit_sim():
    print("exiting cybergrid...")
    exit()


#### tkinter setup
root = tk.Tk()
root.title('cybergrid')

#### canvas and background
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image = tk.PhotoImage(file='background.gif')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

#### frames
node_frame = tk.Frame(root, bg='orange')
node_frame.place(relx=0.025, rely=0.15, relwidth=0.45, relheight=0.35)

PMU_frame = tk.Frame(root, bg='blue', bd=5)
PMU_frame.place(relx=0.525, rely=0.15, relwidth=0.45, relheight=0.35)

map_frame = tk.Frame(root, bg='yellow', bd=5)
map_frame.place(relx=0.025, rely=0.55, relwidth=0.45, relheight=0.35)

attack_frame = tk.Frame(root, bg='green', bd=5)
attack_frame.place(relx=0.525, rely=0.55, relwidth=0.45, relheight=0.35)

#### labels
label = tk.Label(root, text="CONTROL CENTER", bg='red', font=('consolas', 25))
label.place(x=25, y=25, relwidth=0.3, relheight=0.1)

#### buttons
# reset
button1 = tk.Button(root, text="RESET", font=('consolas', 20), fg='red', command=reset_sim)
button1.place(relx=0.8, relwidth=0.1, relheight=0.1)
# exit
button2 = tk.Button(root, text="EXIT", font=('consolas', 20), fg='red', command=exit_sim)
button2.place(relx=0.9, relwidth=0.1, relheight=0.1)

#### main tkinter loop
root.mainloop()
