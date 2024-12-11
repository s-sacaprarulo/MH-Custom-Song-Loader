import sys
import tkinter as tk
import time

#file paths
SCHOOL_FILE_PATH = "C:/Users/1042113/Desktop/Cloned Repositories/ForFun/Test.json"
MAIN_PC_TEST_FILE_PATH = "C:/Users/santi/OneDrive/Desktop/Cloned Repositories/ForFun/Test.json"
PC_HELLSINGER_FILE_PATH = "C:/Program Files (x86)/Steam/steamapps/common/Metal Hellsinger/Metal_Data/StreamingAssets/customsongs.json"
VR_HELLSINGER_FILE_PATH = "C:/Program Files (x86)/Steam/steamapps/common/MetalHellsingerVR/MetalVR_Data/StreamingAssets/customsongs.json"

JSON_FILE_LOCATION:str = PC_HELLSINGER_FILE_PATH

LIST_SONG_BANK_FILE = 0
LIST_SONG_ACT_CODE = 1
LIST_SONG_BPM = 2
LIST_SONG_OFFSET = 3

INTRO_CONST:str = "{\"customLevelMusic\" : ["
OUTRO_CONST:str = "]}"

HELL_LIST:list[str] = {"Voke", "Stygia", "Yhelm", "Incaustis", "Gehenna", "Nihil", "Acheron", "Sheol"}
BASE_OFFSET:str = "0.06"

#codes for the different types of songs
NOACTBANKCODE:str = "{95972dee-fd3a-4a5c-9024-8f714883936e}"

#key is the song name
#list is the following: bank file, bank code, bpm, offset
SONG_DICT:dict[list[str]] = {"Gold" : ["GoldBank",NOACTBANKCODE,"155", "0.16"],
                             "Halo" : ["HaloBank",NOACTBANKCODE,"80","0.06"],
                             "Strangers" : ["StrangersBank",NOACTBANKCODE,"150","0.06"],
                             "NightFall" : ["NightFallBank",NOACTBANKCODE,"192","0.3"],
                             "IfYouCantHang" : ["IfYouCantHangBank",NOACTBANKCODE,"192","0.6"],
                             "TheThingsWeBelieveIn" : ["TheThingsWeBelieveInBank",NOACTBANKCODE,"122","0.06"],
                             "HopeIsTheThingWithFeathers" : ["HopeIsTheThingWithFeathersBank",NOACTBANKCODE,"128","0.06"], #as elliott wanted >:(
                             "CrabRave" : ["CrabRaveBank", NOACTBANKCODE, "125", "0.06"],
                             "Weak" : ["WeakBank", NOACTBANKCODE, "124", "0.06"]}

ACTION_DICT:dict = {"load" : lambda : load_level(),
                    "kill" : lambda : kill()}


#creates a string for a specific song for a given hell
#raises an exception if the hell or custom song do not exist
def create_custom_song_string(hell:str, main_song:str, boss:bool = False) -> str:
    if not hell in HELL_LIST:
        raise Exception("Hell not found! (did you misspell the hell?)")
    try:
        SONG_DICT[main_song]
    except:
        raise Exception("Song not found! (did you misspell it or not import it into python?)")
    level_name_str = f"\"LevelName\" : \"{hell}\","
    Bank_str = "\"Bank\" : \"" + SONG_DICT.get(main_song)[LIST_SONG_BANK_FILE] +"\","
    event_str = "\"Event\" : \"" + SONG_DICT.get(main_song)[LIST_SONG_ACT_CODE] + "\","
    low_hp_event_str = "\"LowHealthBeatEvent\" : \"" + SONG_DICT.get(main_song)[LIST_SONG_ACT_CODE] + "\","
    offset_str = "\"BeatInputOffset\" : " + SONG_DICT.get(main_song)[LIST_SONG_OFFSET] + ","
    bpm_str = "\"BPM\" : " + SONG_DICT.get(main_song)[LIST_SONG_BPM]
    main_level_music = "{" + level_name_str + "\"MainMusic\" : {" + Bank_str + event_str + low_hp_event_str + offset_str + bpm_str + "}"

    boss_level_music = ""
    if boss:
        boss_bank = "\"Bank\" : \"" + SONG_DICT.get(main_song)[LIST_SONG_BANK_FILE] +"\","
        boss_event = "\"Event\" : \"" + SONG_DICT.get(main_song)[LIST_SONG_ACT_CODE] + "\","
        boss_low_hp = "\"LowHealthBeatEvent\" : \"" + SONG_DICT.get(main_song)[LIST_SONG_ACT_CODE] + "\","
        boss_offset = "\"BeatInputOffset\" : " + SONG_DICT.get(main_song)[LIST_SONG_OFFSET] + ","
        boss_bpm = "\"BPM\" : " + SONG_DICT.get(main_song)[LIST_SONG_BPM]
        boss_level_music = ",\"BossMusic\" : {" + boss_bank + boss_event + boss_low_hp + boss_offset + boss_bpm + "}"

    return main_level_music + boss_level_music + "}"

#creates a custom song in the console
def load_level():
    
    #get input hell and make sure it exists
    hell = ""
    while hell == "":
        hell = input("Enter a hell: ")
        if not hell in HELL_LIST:
            print("Not in the Hell list (Case sensitive)")
            hell = ""
    
    #get input song and make sure it exists
    song = ""
    while song == "":
        song = input("Enter a song: ")
        try:
            SONG_DICT[song]
        except:
            print("Not in the song list (did you misspell it or forget to import it into python?)")
            song = ""

    #check if the song should be played during the boss
    out = ""
    boss:bool = False
    while out == "":
        out = input("Should the song play in the boss battle as well? (y/n): ")
        if out == "y":
            boss = True
        elif out == "n":
            boss = False
        else:
            print("Unknown input. Type in y or n.")
            out = ""
    #create and import the song
    time_start = time.time()
    try:
        songs_string = "" #defaults to an empty string so the game doesn't crash if the code errors for some reason
        songs_string = create_custom_song_string(hell, song, boss)
        with open(JSON_FILE_LOCATION, "w") as file:
            file.write(INTRO_CONST + songs_string + OUTRO_CONST)
        time_end = time.time()
        print(f"Operation completed successfully in {time_end - time_start} seconds!")
    except Exception as e:
        time_end = time.time()
        print(f"Operation failed in {time_end - time_start} seconds with excpetion {e}")

    
# action to kill the program
def kill():
    output = input("Are you sure? (Type 'yes' to continue or anything else to abort): ")
    if output == "yes":
        sys.exit()

while True:

    command = input("Give a command: ")
    try:
        ACTION_DICT[command]()
    except Exception as e:
        print(f"Unknown command OR an error occured: {e}")
        pass
