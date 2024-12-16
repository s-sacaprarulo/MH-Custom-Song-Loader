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
        print("Lose")
        pygame.mixer.init()
        sound = pygame.mixer.Sound("C:/Users/1042113/Desktop/Cloned Repositories/ForFun/soundeffectLIB/Taco Bell Bong - Sound Effect (HD).mp3")
        sound.play()

        time.sleep(1.2)
        # os.system("shutdown /r /t 0") # shuts down the system if not commented
        output = messagebox.askyesno("Gambling", "You Suck")
        if output:
            temp_function()

    elif number == 1:
        print("Win")
        pygame.mixer.init()
        sound = pygame.mixer.Sound("C:/Users/1042113/Desktop/Cloned Repositories/ForFun/soundeffectLIB/onlymp3.to - vine_boom-_vBVGjFdwk4-192k-1708393618.mp3")
        sound.play()

        time.sleep(1.2)
        output = messagebox.askyesno("Gambling", "GG EZ")
        if output:
            temp_function()

root = tk.Tk()
root.title("Gamble")
root.geometry("400x300+100+100")
root.wm_attributes("-topmost", 1)

button = tk.Button(root, text="Press at your own risk!", command=lambda: temp_function())
button.pack(pady=20)


root.mainloop()

