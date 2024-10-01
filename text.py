import random
from typing import List
import tkinter as tk
from tkinter import messagebox
import os
import time

def move_window():
    window_hit_time = time.time()
    root.geometry(f"+{random.randrange(0, screen_x)}+{random.randrange(0, screen_y)}")


# Create the root window
root = tk.Tk()

start_time = time.time()
window_width = 200
window_height = 150
screen_x = 1920 - window_width - 500
screen_y = 1200 - window_height - 400


# Set the initial position of the window (e.g., 100x100)
root.geometry("400x300+100+100")

# Add a button to trigger window movement
move_button = tk.Button(root, text="EXTEND YOUR PC'S LIVE BY 3 SECONDS", command=move_window)
move_button.pack(pady=20)


lost = False
window_hit_time = start_time

while not lost:
    curr_time = time.time()
    if (curr_time - window_hit_time > 3):
        lost = True
        break
    # Run the window's event loop
    root.mainloop()

if lost:
    result = messagebox.askokcancel("Virus", "you suck")

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
