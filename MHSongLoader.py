import json
import tkinter as tk

school_file_path = "C:/Users/1042113/Desktop/Cloned Repositories/ForFun/Test.json"
main_pc_test_file_path = "C:/Users/santi/OneDrive/Desktop/Cloned Repositories/ForFun/Test.json"
pc_Hellsinger_file_path = "C:/Program Files (x86)/Steam/steamapps/common/Metal Hellsinger/Metal_Data/StreamingAssets/customsongs.json"
vr_Hellsinger_file_path = "C:/Program Files (x86)/Steam/steamapps/common/MetalHellsingerVR/MetalVR_Data/StreamingAssets/customsongs.json"

json_file_location:str = main_pc_test_file_path

INTRO_CONST:str = "{\"customLevelMusic\" : ["
OUTRO_CONST:str = "]}"

#hell list
#Leviathan is leviathan mode
HELL_LIST:list[str] = {"Voke", "Stygia", "Yhelm", "Incaustis", "Gehena", "Nihil", "Acheron", "Sheol", "Levaithan"}
BASE_OFFSET:str = "0.06"

#codes for the different types of songs
NOACTBANKCODE:str = "{95972dee-fd3a-4a5c-9024-8f714883936e}"

#The song files for all the different custom songs
song_file_dict:dict = {"John Doe" : "FilePathForJohnDoe",
                       "Halo" : "FilePathForHalo"}

#SongKey dict
song_key_dict:dict = {"John Doe" : NOACTBANKCODE}

#bpm for each song
song_bpm_dict:dict = {"John Doe" : "120"}

#bpm offset for each song
song_offset_dict:dict = {"John Doe" : "0.06"}

#creates a string for a specific song for a given hell
#raises an exception if the hell or custom song do not exist
def create_custom_song_string(hell:str, song:str) -> str:
    if not hell in HELL_LIST:
        raise Exception("Hell not found!")
    
    
songs_string = ""   
try:
    songs_string = create_custom_song_string("sjfkldds", "209324")
except:
    pass

with open(json_file_location, "w") as file:
    file.write(INTRO_CONST + songs_string + OUTRO_CONST)