import json
import tkinter as tk

json_file_location:str = "C:/Users/1042113/Desktop/Cloned Repositories/ForFun/Test.json"

HELL_LIST:list[str] = {"Voke", "Stygia", "Yhelm", "Incaustis", "Gehnna", "Nihl", "Acheron", "Sheol", "Levaithan"}
BASE_OFFSET:str = "0.06"

song_file_dict:dict = {"John Doe" : "FilePathForJohnDoe",
                       "Halo" : "FilePathForHalo"}

song_key_dict:dict = {"John Doe" : "{wier234092812}"}

song_bpm_dict:dict = {"John Doe" : "120"}

song_offset_dict:dict = {"John Doe" : "0.06"}

def create_custom_song_string(hell:str, song:str):
    if not hell in HELL_LIST:
        raise Exception("Hell not found!")
    
try:
    create_custom_song_string("sjfkldds", "209324")
except:
    pass

with open(json_file_location, "w") as file:
    file.write("{\n" + song_file_dict.get("Yhelm") + " \n}")