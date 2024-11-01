import random
from typing import List
from typing import Dict
import tkinter as tk
from tkinter import messagebox
import threading
import os
import time
import pygame

__numberplayers__ = 2

def shot_fired(bullet_chambers:int, player_turn:int):
    number = random.randint(1, 6)

    if number <= bullet_chambers:
        print("Lose")
        pygame.mixer.init()
        sound = pygame.mixer.Sound("C:/Users/1042113/Desktop/Cloned Repositories/ForFun/soundeffectLIB/Taco Bell Bong - Sound Effect (HD).mp3")
        sound.play()

        time.sleep(1.2)
        # os.system("shutdown /r /t 0") # shuts down the system if not commented
        next_player = get_next_player_up(player_turn)
        output = messagebox.askyesno("Russian Roulette", f"player {player_turn} dead! Player {next_player}'s turn!")
        if output:
            shot_fired(1, next_player)

    else:
        print("Win")
        pygame.mixer.init()
        sound = pygame.mixer.Sound("C:/Users/1042113/Desktop/Cloned Repositories/ForFun/soundeffectLIB/onlymp3.to - vine_boom-_vBVGjFdwk4-192k-1708393618.mp3")
        sound.play()

        time.sleep(1.2)
        next_player = get_next_player_up(player_turn)
        output = messagebox.askyesno("Russian Roulette", f"Player {next_player}'s turn!")
        if output:
            shot_fired(bullet_chambers + 1, next_player)


def get_next_player_up(current_player:int):
    if current_player == __numberplayers__:
        return 1
    return current_player+1

# setting up the window
root = tk.Tk()
root.title("Russian Roulette")
root.geometry("400x300+100+100")
root.wm_attributes("-topmost", 1)

starting_player = random.randint(1, __numberplayers__)

button = tk.Button(root, text=f"Player {starting_player} commences!", command=lambda: shot_fired(1, starting_player))
button.pack(pady=20)


root.mainloop()