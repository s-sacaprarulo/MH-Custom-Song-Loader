import random
from typing import List
import tkinter as tk
from tkinter import messagebox
import threading
import os
import time
import pygame
# from playsound import playsound


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
    window_width = 500
    window_height = 350
    screen_x = 2100 - window_width - 700
    screen_y = 1400 - window_height - 400
    root.geometry(f"+{random.randrange(0, screen_x)}+{random.randrange(0, screen_y)}")
    game_time.update_flag_time()

def open_window():
    #setting up the window
    root = tk.Tk()
    root.title("VIRUS")
    root.geometry("400x300+100+100")
    root.wm_attributes("-topmost", 1)

    # Add a button to trigger window movement
    move_button = tk.Button(root, text="EXTEND YOUR PC'S LIVE BY 3 SECONDS", command=lambda: move_window(root))
    move_button.pack(pady=20)


    root.after(10, lambda:update_timer(root))
    root.mainloop()

def update_timer(root:tk):
    root.title(game_time.flag_time + 3 - game_time.curr_time)

# def on_closing():
#    print("CLOSED WINDOW")
    
# Start the Tkinter window in a separate thread
window_thread = threading.Thread(target=open_window)
window_thread.start()

lost = False
no_restart = True

while not lost:
    game_time.update_curr_time()
    if (game_time.is_over_time()):
        lost = True
        break
    time.sleep(0.01)

if lost:
    messagebox.askokcancel("Virus", "you suck")

    result = messagebox.askyesno("Virus", "YOU HAVE LOST THE GAME! we would restart the computer now, but the debug option is on so we wont. Do you still want to restart it?")
    if (result):
        result = messagebox.askyesno("Virus", "ARE YOU SURE? this will restart your computer and any unsaved datat will be lost!")
        if (result):
            pygame.mixer.init()
            sound = pygame.mixer.Sound("C:/Users/1042113/Desktop/Cloned Repositories/ForFun/soundeffectLIB/Metal pipe falling sound effect(loud).mp3")
            sound.play()
            # pygame.time.delay(1200)
            time.sleep(1.2)
            print("RESTART")
            if not no_restart:
                os.system("shutdown /r /t 0")





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
