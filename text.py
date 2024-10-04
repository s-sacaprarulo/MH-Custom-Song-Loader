import random
from typing import List
import tkinter as tk
from tkinter import messagebox
import threading
import os
import time
import pygame
# from playsound import playsound

# a Timer class used to calculate whether or not the game is lost
class PersonalTimer:

    #constructor - passes an amount of seconds until the game is lost
    def __init__(self, max_time):
        self.flag_time = time.time() + max_time
        self.curr_time = time.time()
        self.max_time = max_time
    
    """sets the time difference to the current time"""
    def update_flag_time(self):
        self.flag_time = time.time()

    """sets the current time to... the current time"""
    def update_curr_time(self):
        self.curr_time = time.time()

    """checks if the game should be lost using time and flagtime
    returns false if the game is not lost, and true if it is"""
    def is_over_time(self) -> bool:
        if self.curr_time > self.flag_time + self.max_time:
            return True
        return False

# creating our gametime object
game_time = PersonalTimer(3)

# the function that the button on the window runs
def move_window(root:tk):
    # window constants
    window_width = 500
    window_height = 350

    #window movement range
    screen_x = 2100 - window_width - 700
    screen_y = 1400 - window_height - 400
    
    #actually moving the window
    root.geometry(f"+{random.randrange(0, screen_x)}+{random.randrange(0, screen_y)}")

    #updating the flagtime variable
    game_time.update_flag_time()

# sets up and opens up the game window
def open_window():
    #setting up the window
    root = tk.Tk()
    root.title("VIRUS")
    root.geometry("400x300+100+100")
    root.wm_attributes("-topmost", 1)

    # Add a button to trigger window movement
    move_button = tk.Button(root, text="EXTEND YOUR PC'S LIVE BY 3 SECONDS", command=lambda: move_window(root))
    move_button.pack(pady=20)

    # run the window's mainloop
    root.after(10, lambda: update_timer(root))
    root.mainloop()

def show_loss_window():
    messagebox.askokcancel("Virus", "you suck")

# (in theroey) sets the window's title to be the time left
def update_timer(root:tk):
    root.title(game_time.flag_time + 3 - game_time.curr_time)
    
# Start the Tkinter window in a separate thread
window_thread = threading.Thread(target=open_window)
window_thread.start()

# creating variables
lost = False
no_restart = True # no restart variable prevents the computer from restarting if you lose. Set to false to enable this option

# main gameloop
while not lost:
    #update the timer
    game_time.update_curr_time()
    #check if the timer is over what it should be
    if (game_time.is_over_time()):
        # ends the game if so
        lost = True
        break
    time.sleep(0.01)

# runs the lost message
if lost:
    #TODO: multithread the showlosswindow textbox
    text_box_thread = threading.Thread(target=show_loss_window)
    text_box_thread.start()

    #debug option, runs a window asking whether or not the computer should restart
    result = messagebox.askyesno("Virus", "YOU HAVE LOST THE GAME! we would restart the computer now, but the debug option is on so we wont. Do you still want to restart it?")
    if (result):
        result = messagebox.askyesno("Virus", "ARE YOU SURE? this will restart your computer and any unsaved datat will be lost!")
        if (result):
            # plays metal pipe.sfx on loss
            pygame.mixer.init()
            sound = pygame.mixer.Sound("C:/Users/1042113/Desktop/Cloned Repositories/ForFun/soundeffectLIB/Metal pipe falling sound effect(loud).mp3")
            sound.play()

            # wait 1.2s
            time.sleep(1.2)

            #restarts the pc if no_restart is false
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
