import random
from typing import List
import tkinter as tk
from tkinter import messagebox
import threading
import os
import time


class PersonalTimer:
    def __init__(self, max_time):
        self.flag_time = time.time() + max_time
        self.curr_time = time.time()
        self.max_time = max_time
    
    def update_flag_time(self):
        self.flag_time = time.time()

    def update_curr_time(self):
        self.curr_time = time.time()

    def is_over_time(self):
        if self.curr_time > self.flag_time + self.max_time:
            return True
        return False


game_time = PersonalTimer(3)


def move_window(root:tk):
    window_width = 200
    window_height = 150
    screen_x = 1920 - window_width - 500
    screen_y = 1200 - window_height - 400
    root.geometry(f"+{random.randrange(0, screen_x)}+{random.randrange(0, screen_y)}")
    game_time.update_flag_time()

def open_window():
    root = tk.Tk()
    # Set the initial position of the window (e.g., 100x100)
    root.geometry("400x300+100+100")
    

    # Add a button to trigger window movement
    move_button = tk.Button(root, text="EXTEND YOUR PC'S LIVE BY 3 SECONDS", command=lambda: move_window(root))
    move_button.pack(pady=20)

    root.mainloop()

# Start the Tkinter window in a separate thread
window_thread = threading.Thread(target=open_window)
window_thread.start()


lost = False

while not lost:
    game_time.update_curr_time()
    if (game_time.is_over_time()):
        lost = True
        break

if lost:
    messagebox.askokcancel("Virus", "you suck")

    result = messagebox.askyesno("Virus", "YOU HAVE LOST THE GAME! we would restart the computer now, but the debug option is on so we wont. Do you still want to restart it?")
    if (result):
        result = messagebox.askyesno("Virus", "ARE YOU SURE? this will restart your computer and any unsaved datat will be lost!")
        if (result):
            print("RESTART")
            # restarts the computer if uncommented
            os.system("shutdown /r /n 0")





'''
# Create the main window
root = tk.Tk()

# Set the window title
root.title("My Window")



window_x:int = 500
window_y:int = 500
root.geometry(f"+{window_x}+{window_y}")



if result:
    os.system("shutdown /r /t 0")
else:
    new_result = messagebox.askokcancel("Virus", "NO LOL I'M KILLING IT ANYWAY")
    if new_result:
        os.system("shutdown /r /t 0")
    else:
        os.system("shutdown /r /t 0")
'''
