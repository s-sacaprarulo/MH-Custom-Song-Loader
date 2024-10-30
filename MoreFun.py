import random
from typing import List
from typing import Dict
import tkinter as tk
from tkinter import messagebox
import threading
import os
import time
import pygame


def temp_function():
    number = random.randint(0, 1)
    if number == 0:
        print("0")
        # os.system("shutdown /r /t 0") # shuts down the system if not commented
        output = messagebox.askyesno("Gambling", "You lost, Shutdown code is inactive. Want to try again?")
        if output:
            temp_function()

    elif number == 1:
        print("1")
        output = messagebox.askyesno("Gambling", "Why did you do that? Want to do it again?")
        if output:
            temp_function()

root = tk.Tk()
root.title("Gamble")
root.geometry("400x300+100+100")
root.wm_attributes("-topmost", 1)

button = tk.Button(root, text="Press at your own risk!", command=lambda: temp_function())
button.pack(pady=20)


root.mainloop()

