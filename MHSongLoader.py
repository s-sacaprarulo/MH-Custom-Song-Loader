import json
import tkinter as tk

#file paths
SCHOOL_FILE_PATH = "C:/Users/1042113/Desktop/Cloned Repositories/ForFun/Test.json"
MAIN_PC_TEST_FILE_PATH = "C:/Users/santi/OneDrive/Desktop/Cloned Repositories/ForFun/Test.json"
PC_HELLSINGER_FILE_PATH = "C:/Program Files (x86)/Steam/steamapps/common/Metal Hellsinger/Metal_Data/StreamingAssets/customsongs.json"
VR_HELLSINGER_FILE_PATH = "C:/Program Files (x86)/Steam/steamapps/common/MetalHellsingerVR/MetalVR_Data/StreamingAssets/customsongs.json"

JSON_FILE_LOCATION:str = SCHOOL_FILE_PATH

INTRO_CONST:str = "{\"customLevelMusic\" : ["
OUTRO_CONST:str = "]}"

#hell list
#Leviathan is leviathan mode
HELL_LIST:list[str] = {"Voke", "Stygia", "Yhelm", "Incaustis", "Gehenna", "Nihil", "Acheron", "Sheol", "Leviathan"}
BASE_OFFSET:str = "0.06"

#codes for the different types of songs
NOACTBANKCODE:str = "{95972dee-fd3a-4a5c-9024-8f714883936e}"

#The song files for all the different custom songs
SONG_FILE_DICT:dict = {"Gold" : "GoldBank",
                       "Halo" : "HaloBank",
                       "Strangers" : "StrangersBank",
                       "NightFall" : "NightFallBank",
                       "IfYouCantHang" : "IfYouCantHangBank",
                       "TheThingsWeBelieveIn" : "TheThingsWeBelieveInBank",
                       "HopeIsTheThingWithFeathers" : "HopeIsTheThingWithFeathersBank"}

#SongKey dict
SONG_KEY_DICT:dict = {"Gold" : NOACTBANKCODE,
                      "Halo" : NOACTBANKCODE,
                      "Strangers" : NOACTBANKCODE,
                       "NightFall" : NOACTBANKCODE,
                       "IfYouCantHang" : NOACTBANKCODE,
                       "TheThingsWeBelieveIn" : NOACTBANKCODE,
                       "HopeIsTheThingWithFeathers" : NOACTBANKCODE}

#bpm for each song
SONG_BPM_DICT:dict = {"Gold" : "155",
                      "Halo" : "80",
                      "Strangers" : "150",
                      "NightFall" : "192",
                      "IfYouCantHang" : "192",
                      "TheThingsWeBelieveIn" : "122",
                      "HopeIsTheThingWithFeathers" : "128"}

#bpm offset for each song
SONG_OFFSET_DICT:dict = {"Gold" : "0.16",
                         "Halo" : "0.06",
                         "Strangers" : "0.4",
                         "NightFall" : "0.3",
                         "IfYouCantHang" : "0.6",
                         "TheThingsWeBelieveIn" : "0.06",
                         "HopeIsTheThingWithFeathers" : "0.06"}

#creates a string for a specific song for a given hell
#raises an exception if the hell or custom song do not exist
def create_custom_song_string(hell:str, song:str) -> str:
    if not hell in HELL_LIST:
        raise Exception("Hell not found! (did you misspell the hell?)")
    if not song in SONG_FILE_DICT:
        raise Exception("Song not found! (did you import it into python?)")
    level_name_str = f"\"LevelName\" : \"{hell}\","
    Bank_str = "\"Bank\" : \"" + SONG_FILE_DICT.get(song) +"\","
    event_str = "\"Event\" : \"" + SONG_KEY_DICT.get(song) + "\","
    low_hp_event_str = "\"LowHealthBeatEvent\" : \"" + SONG_KEY_DICT.get(song) + "\","
    offset_str = "\"BeatInputOffset\" : " + SONG_OFFSET_DICT.get(song) + ","
    bpm_str = "\"BPM\" : " + SONG_BPM_DICT.get(song)
    main_level_music = "{" + level_name_str + "\"MainMusic\" : {" + Bank_str + event_str + low_hp_event_str + offset_str + bpm_str + "}}"
    return main_level_music
    
songs_string = ""   
#input("ask")
try:
    songs_string = create_custom_song_string("Acheron", "Gold")
except Exception as e:
    print(e)
    pass

with open(JSON_FILE_LOCATION, "w") as file:
    file.write(INTRO_CONST + songs_string + OUTRO_CONST)