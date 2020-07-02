#
# cybergrid:
# microgrid security simulation software
#
# carter trafton & misha kharitonov
# wit 2020 - senior design
#
import tkinter as tk
from gui import GUI


def cg():
    print("here it is, here is cybergrid:")
    print(".-'^`\                                        /`^'-.")
    print(".'   ___\                                      /___   `.")
    print("/    /.---.                                    .---.\    ")
    print("|    //     '-.  ___________________________ .-'     \    |")
    print("|   ;|         \/--------------------------//         |;   |")
    print("\   ||       |\_)                          (_/|       ||   /")
    print("\  | \  . \ ;  |                          || ; / .  / |  /")
    print("'\_\ \ \ \ \ |          CyberGrid       ||/ / / // /_/'")
    print("    \ \ \ \|                          |/ / / /")
    print("     `'-\_\_\                          /_/_/-'`")
    print("            '--------------------------'")
    return


if __name__ == "__main__":

    #### pre mainloop
    print("Starting CyberGrid...\n\n")

    cg()

    #### tkinter setup
    root = tk.Tk()
    root.title('CyberGrid')

    #### creating GUI
    GUI(root).pack(side="top", fill="both", expand=True)
    while True:

        try:
            #### GUI updating
            root.update_idletasks()
            root.update()  # update the GUI
        except:
            exit()


