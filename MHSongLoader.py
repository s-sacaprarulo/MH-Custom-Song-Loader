import sys
import os
import tkinter as tk
from tkinter import StringVar
import time
import pygame
import threading

#file paths
SCHOOL_FILE_PATH = "C:/Users/1042113/Desktop/Cloned Repositories/ForFun/Test.json"
MAIN_PC_TEST_FILE_PATH = "C:/Users/santi/OneDrive/Desktop/Cloned Repositories/ForFun/Test.json"
PC_HELLSINGER_FILE_PATH = "C:/Program Files (x86)/Steam/steamapps/common/Metal Hellsinger/Metal_Data/StreamingAssets/customsongs.json"
VR_HELLSINGER_FILE_PATH = "C:/Program Files (x86)/Steam/steamapps/common/MetalHellsingerVR/MetalVR_Data/StreamingAssets/customsongs.json"

PC_ENABLED_FILE = "C:/Program Files (x86)/Steam/steamapps/common/Metal Hellsinger/Metal_Data/StreamingAssets/customsongs.json"
PC_DISABLED_FILE = "C:/Program Files (x86)/Steam/steamapps/common/Metal Hellsinger/Metal_Data/StreamingAssets/inactive_customsongs.json"

TEST_ENABLED_FILE = "Test.json"
TEST_DISABLED_FILE = "in_Test.json"

JSON_FILE_LOCATION:str = PC_HELLSINGER_FILE_PATH
FILE_NAME:str = PC_ENABLED_FILE
DEACTIVATED_FILE_NAME:str = PC_DISABLED_FILE

LIST_SONG_BANK_FILE = 0
LIST_SONG_ACT_CODE = 1
LIST_SONG_BPM = 2
LIST_SONG_OFFSET = 3
LIST_SONG_PREVIEW_SUBLIST = 4
LIST_SONG_ARTIST = 5

PREVIEW_SONG_FILE = 0
PREVIEW_SONG_START_TIME = 1
PREVIEW_SONG_DURATION = 2

INTRO_CONST:str = "{\"customLevelMusic\" : ["
OUTRO_CONST:str = "]}"

HELL_LIST:list[str] = ["Voke", "Stygia", "Yhelm", "Incaustis", "Gehenna", "Nihil", "Acheron", "Sheol"]
HELL_DESCRIPTION:dict[list[str]] = {
                            "Voke":"Voke was the spot I spent time closest to. So many years adjacent to all that frozen awfulness, the cold seeps into your bones. Can only imagine what it's like to be locked up there forever.",
                            "Stygia":"Stygia. Lot of spiritual electricity, if you take my meaning, the kind the Judge just hrived on. Along with the lightning, there were some things in the shadows here who knew no master.",
                            "Yhelm":"If you wanted to ask this Skull what real Hell would be for him, the I guess I'd say Yhelm. Souls here, cursed to be isolated from each other. Hard on us extroverts, I'll tell you that.",
                            "Incaustis":"Back before the Unknown showed up this was a key location. Souls doomed for greed here mined eternally for brass and iron and whatnot, and a host of squabbling minor demons with aspirations of greatness fought each other for their piece.",
                            "Gehenna":"Gehenna. Sinners here get locked up in tombs forever, guarded by demons. They say it's Hell for folks who uphold unjust laws, or hold up laws unjustly. I guess you could also say it's Hell for claustrophobic folks.",
                            "Nihil":"Nihil was the kind of Hell that wasn't really supposed to exist, kinda airy and cold relative to some others. Stories said it was a kind of proto-Hell, split off from someplace in the Heavens... But demons lie, so the truth is hard to figure.",
                            "Acheron":"In case you were wondering Acheron is pronounced \"Akkeron\". I know, we learn somethin' new every day. Wishful thinkin' maybe, but if we'd dealt different with them infernal cogwheels here, maybe our ride wouldn't have been so rough...",
                            "Sheol":"Sheol ain't like any other Hell. All the others are made for suffering, but Sheol's sort of ground zero for it all. The Red Judge watches over everything from her throne here, waiting for the Unknown, and Heaven's watching. Plus through a quirk of design, it's also the last bulwark separating Heaven from Hell."
}
BASE_OFFSET:str = "0.06"

#codes for the different types of songs
NOACTBANKCODE:str = "{95972dee-fd3a-4a5c-9024-8f714883936e}"

#key is the song name
#list is the following: bank file, bank code, bpm, offset, [preview file, preview start time, preview duration], Artist
SONG_DICT:dict[list[str]] = {"Gold" : ["GoldBank",NOACTBANKCODE,"155", "0.16",["HellsingerSongs/Loi-Gold.ogg",42,40], "Loi"],
                             "Halo" : ["HaloBank",NOACTBANKCODE,"80",BASE_OFFSET,["HellsingerSongs/Beyonce-Halo.mp3", 50, 23], "Beyonce"],
                             "Strangers" : ["StrangersBank",NOACTBANKCODE,"150",BASE_OFFSET,["HellsingerSongs/Dragonforce-Strangers.mp3",51,27], "Dragonforce"],
                             "Night Fall" : ["NightFallBank",NOACTBANKCODE,"192","0.3",["HellsingerSongs/Blind_Guardian-NightFall.mp3",75,23],"Blind Guardian"],
                             "If You Cant Hang" : ["IfYouCantHangBank",NOACTBANKCODE,"192","0.6",["HellsingerSongs/Sleeping_With_Sirens-If_You_Can't_Hang.mp3",75,25], "Sleeping With Sirens"],
                             "The Things We Believe In" : ["TheThingsWeBelieveInBank",NOACTBANKCODE,"122",BASE_OFFSET,["HellsingerSongs/Order_Organ-The_Things_we_believe_in.ogg",89,33], "Order Organ"],
                             "Hope Is The Thing With Feathers" : ["HopeIsTheThingWithFeathersBank",NOACTBANKCODE,"128",BASE_OFFSET,["HellsingerSongs/Shida_Aruya-Hope_Is_the_Thing_With_Feathers.mp3",59,31], "Shida Aruya"], #as elliott wanted >:(
                             "Crab Rave" : ["CrabRaveBank", NOACTBANKCODE, "125", BASE_OFFSET,["HellsingerSongs/Noisestorm-Crab_Rave.mp3",74,33], "Noisestorm"],
                             "Weak" : ["WeakBank", NOACTBANKCODE, "124", BASE_OFFSET,["HellsingerSongs/AJR-Weak.ogg",32,32], "AJR"]}

ACTION_DICT:dict = {"load" : lambda : load_level(),
                    "kill" : lambda : kill(),
                    "attach" : lambda : attach_script(),
                    "deattach" : lambda : deattach_script(),
                    "list" : lambda : print_list()}


#creates a string for a specific song for a given hell
#raises an exception if the hell or custom song do not exist
def create_custom_song_string(hell:str, main_song:str, boss:bool = True) -> str:
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

#creates a custom song in the console and adds it to customsongs.json
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

        # This first check is to check if the file actually exists.
        # We dont need to read the file, but if we try to write to a file that doesn't exist, it will create a new file
        # this will throw an exception if the file does not exist and, thus, not overwrite it
        with open(JSON_FILE_LOCATION, "r") as file:
            pass
        with open(JSON_FILE_LOCATION, "w") as file:
            file.write(INTRO_CONST + songs_string + OUTRO_CONST)
        time_end = time.time()
        print(f"Operation completed successfully in {time_end - time_start} seconds!")
    except Exception as e:
        time_end = time.time()
        print(f"Operation failed in {time_end - time_start} seconds with excpetion {e}\n(This may be because the custom songs are not attached run 'attach' to attach them. Or the file location may be incorrect)")

#Attaches the customsongs.json file to Hellsinger by renaming the file back to 'customsongs.json'
#This is so modded songs can be played once more without resetting the game
def attach_script():
    start_time = time.time()
    try:
        try:
            with open(DEACTIVATED_FILE_NAME, "r") as file:
                pass
        except Exception as e:
            end_time = time.time()
            print(f"Operation failed in {end_time - start_time} seconds because the file is already attached!")
            return
        os.rename(DEACTIVATED_FILE_NAME, FILE_NAME)
        end_time = time.time()
        print(f"Operation successful in {end_time - start_time} seconds!")
    except Exception as e:
        end_time = time.time()
        print(f"Operation failed in {end_time - start_time} seconds with error {e} \n(this may be because the file is already attached or the wrong file is set as the location)")

#Deattaches the customsongs.json file from Hellsinger by renaming the file
#This is so vanila songs can be played without resetting the game
def deattach_script():
    start_time = time.time()
    try:
        try:
            with open(FILE_NAME, "r") as file:
                pass
        except Exception as e:
            end_time = time.time()
            print(f"Operation failed in {end_time - start_time} seconds because the file is already deattached!")
            return
        os.rename(FILE_NAME, DEACTIVATED_FILE_NAME)
        end_time = time.time()
        print(f"Operation successful in {end_time - start_time} seconds!")
    except Exception as e:
        end_time = time.time()
        print(f"Operation failed in {end_time - start_time} seconds with error {e} \n(this may be because the file is already deattached or the wrong file is set as the location)")

#Prints out the hells and songs
def print_list():
    print(f"Hells: 'Voke', 'Stygia', 'Yhelm', 'Incaustis', 'Gehenna', 'Nihil', 'Acheron', 'Sheol'\nSongs: {list(SONG_DICT.keys())}")

#Kills the program
def kill():
    output = input("Are you sure? (Type 'yes' to continue or anything else to abort): ")
    if output == "yes":
        sys.exit()

#function for selecting a dropdown item
def on_select(selected_song):
    if selected_song in HELL_LIST:
        chosen_level_config[0] = selected_song
        update_hell_stats()
    elif selected_song in SONG_DICT:
        chosen_level_config[1] = selected_song
        update_song_stats()

#When you hit the load button
def load_level_without_prompts():
    time_start = time.time()
    try:
        songs_string = "" #defaults to an empty string so the game doesn't crash if the code errors for some reason
        songs_string = create_custom_song_string(chosen_level_config[0], chosen_level_config[1])

        # This first check is to check if the file actually exists.
        # We dont need to read the file, but if we try to write to a file that doesn't exist, it will create a new file
        # this will throw an exception if the file does not exist and, thus, not overwrite it
        with open(JSON_FILE_LOCATION, "r") as file:
            pass
        with open(JSON_FILE_LOCATION, "w") as file:
            file.write(INTRO_CONST + songs_string + OUTRO_CONST)
        time_end = time.time()
        print(f"Operation completed successfully in {time_end - time_start} seconds!")
    except Exception as e:
        time_end = time.time()
        print(f"Operation failed in {time_end - time_start} seconds with excpetion {e}\n(This may be because the custom songs are not attached run 'attach' to attach them. Or the file location may be incorrect)")

#Preview song
def preview_song():
    # will stop the previous audio track if it exists
    try:
        pygame.mixer.music.stop()
    except:
        pass
    #gets the song preview
    song:list[str] = SONG_DICT.get(chosen_level_config[1])[LIST_SONG_PREVIEW_SUBLIST]
    #plays the preview
    pygame.mixer.init()
    pygame.mixer.music.load(song[PREVIEW_SONG_FILE])
    pygame.mixer.music.play(start=song[PREVIEW_SONG_START_TIME])
    playing_preview_song[0] = chosen_level_config[1]
    #(heres where it gets complicated)
    #creates a second thread to stop the song after its duration time
    #this thread goes to a different function
    stop_thread = threading.Thread(target=_stop_after_preview_time, args=(song[PREVIEW_SONG_DURATION],))
    stop_thread.start()

#will attempt to stop the preview of a song
def stop_preview():
    try:
        pygame.mixer.music.stop()
    except:
        print("unable to stop because nothing is playing! (or no mixer is created)")

#multithread comes to this fuction to stop the song after a certain amount of time has passed
def _stop_after_preview_time(song_durr:int):
    curr_song = chosen_level_config[1]
    time.sleep(song_durr)
    if (playing_preview_song[0] == curr_song):
        pygame.mixer.music.stop()
#window setup

def update_song_stats():
    song = SONG_DICT.get(chosen_level_config[1])
    song_BPM_label.config(text=f"BPM: {song[LIST_SONG_BPM]}")
    song_artist_label.config(text=f"Author: {song[LIST_SONG_ARTIST]}")

def update_hell_stats():
    hell=chosen_level_config[0]
    hell_name_label.config(text=hell)
    hell_description_text_label.config(text=HELL_DESCRIPTION.get(hell))

#root setup
root = tk.Tk()
root.title("MH Custom Song Loader")
root.geometry("500x300")
root.resizable(False,False)

#Labels
label = tk.Label(root, text="METAL HELLSINGER CUSTOM SONG LOADER", font=("Helvetica", 16))
label.pack(side=tk.TOP)
hell_label = tk.Label(root,text="HELL", font=("Helvetica", 12))
song_label = tk.Label(root,text="SONG", font=("Helvetica", 12))
song_options_label = tk.Label(root, text="SONG OPTIONS", font=("Helvetica", 10))
song_stats_label = tk.Label(root, text="SONG STATS", font=("Helvetica", 10))
song_BPM_label = tk.Label(root, text="BPM: n/a")
song_artist_label = tk.Label(root, text="Author: n/a")
hell_name_label = tk.Label(root, text="n/a", font=("Helvetica", 20), anchor="center")
hell_description_text_label = tk.Label(root, text="n/a",wraplength=250)

#Buttons
attach_script_button = tk.Button(root,text="Attach", command=lambda:attach_script())
deattach_script_button = tk.Button(root, text="Deattach", command=lambda:deattach_script())
load_song_button = tk.Button(root, text="LOAD", font=("Helvetica", 30), width=100, height=1, command=lambda:load_level_without_prompts())
preview_button = tk.Button(root, text="Preview", command=lambda:preview_song())
stop_preview_button = tk.Button(root, text="Stop", command=lambda:stop_preview())

#dropdowns
#songs
selected_song = StringVar(root)
selected_song.set(list(SONG_DICT.keys())[0])
song_select_dropdown = tk.OptionMenu(root, selected_song, *SONG_DICT.keys(), command=on_select)
#hells
selected_hell = StringVar(root)
selected_hell.set(list(HELL_LIST)[0])
hell_select_dropdown = tk.OptionMenu(root, selected_hell, *HELL_LIST, command=on_select)

#positioning
load_song_button.pack(side=tk.BOTTOM)
attach_script_button.place(x=390,y=30)
deattach_script_button.place(x=440,y=30)
hell_label.place(x=0,y=65)
hell_select_dropdown.place(x=0,y=90)
song_label.place(x=0, y=130)
song_select_dropdown.place(x=0,y=155)
preview_button.place(x=400,y=100)
stop_preview_button.place(x=460,y=100)
song_options_label.place(x=395,y=80)
song_stats_label.place(x=400,y=140)
song_artist_label.place(x=370, y=160)
song_BPM_label.place(x=370, y=180)
hell_name_label.place(x=180,y=50)
hell_description_text_label.place(x=100,y=100)

chosen_level_config = [HELL_LIST[0], list(SONG_DICT.keys())[0]]
playing_preview_song = [""]

update_song_stats()
update_hell_stats()
root.mainloop()
sys.exit()

#retired command prompt thing

#main loop of the program
while True:
    #gets a command
    command = input(f"Give a command {list(ACTION_DICT.keys())}: ")

    #attempts to execute the command
    try:
        ACTION_DICT[command]()
    
    #if the command errors
    except Exception as e:
        #checks if the error is caused by an invalid command
        if command == e.args[0]:
            print(f"Unknown command!")
        #otherwise prints the error
        else:
            print(f"An error occured: {e}")
