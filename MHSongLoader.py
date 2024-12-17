import sys
import os
import tkinter as tk
from tkinter import StringVar
import time
import pygame
import threading

#file paths
TEST_FILE_PATH = "Test.json"
PC_HELLSINGER_FILE_PATH = "C:/Program Files (x86)/Steam/steamapps/common/Metal Hellsinger/Metal_Data/StreamingAssets/customsongs.json"
VR_HELLSINGER_FILE_PATH = "C:/Program Files (x86)/Steam/steamapps/common/MetalHellsingerVR/MetalVR_Data/StreamingAssets/customsongs.json"

PC_ENABLED_FILE = "C:/Program Files (x86)/Steam/steamapps/common/Metal Hellsinger/Metal_Data/StreamingAssets/customsongs.json"
PC_DISABLED_FILE = "C:/Program Files (x86)/Steam/steamapps/common/Metal Hellsinger/Metal_Data/StreamingAssets/inactive_customsongs.json"

TEST_ENABLED_FILE = "Test.json"
TEST_DISABLED_FILE = "in_Test.json"

JSON_FILE_LOCATION:str = PC_HELLSINGER_FILE_PATH
FILE_NAME:str = PC_ENABLED_FILE 
DEACTIVATED_FILE_NAME:str = PC_DISABLED_FILE

CUSTOM_SONGS_FILE_LOCATION:str = "Custom_Song_List.txt"

LIST_SONG_BANK_FILE = 0
LIST_SONG_ACT_CODE = 1
LIST_SONG_BPM = 2
LIST_SONG_OFFSET = 3
LIST_SONG_PREVIEW_SUBLIST = 4
LIST_SONG_ARTIST = 5

PREVIEW_SONG_FILE = 0
PREVIEW_SONG_START_TIME = 1
PREVIEW_SONG_DURATION = 2

SUCCESS_COLOR = "#00a616"
FAILED_COLOR = "red"
BACKGROUND_COLOR = "#260303"

INTRO_CONST:str = "{\"customLevelMusic\" : ["
OUTRO_CONST:str = "]}"

HELL_LIST:list[str] = ["Voke", "Stygia", "Yhelm", "Incaustis", "Gehenna", "Nihil", "Acheron", "Sheol"]
HELL_DESCRIPTION:dict[list[str]] = {
                            "Voke"     :"Voke was the spot I spent time closest to. So many years adjacent to all that frozen awfulness, the cold seeps into your bones. Can only imagine what it's like to be locked up there forever.",
                            "Stygia"   :"Stygia. Lot of spiritual electricity, if you take my meaning, the kind the Judge just thrived on. Along with the lightning, there were some things in the shadows here who knew no master.",
                            "Yhelm"    :"If you wanted to ask this Skull what real Hell would be for him, then I guess I'd say Yhelm. Souls here, cursed to be isolated from each other. Hard on us extroverts, I'll tell you that.",
                            "Incaustis":"Back before the Unknown showed up this was a key location. Souls doomed for greed here mined eternally for brass and iron and whatnot, and a host of squabbling minor demons with aspirations of greatness fought each other for their piece.",
                            "Gehenna"  :"Gehenna. Sinners here get locked up in tombs forever, guarded by demons. They say it's Hell for folks who uphold unjust laws, or hold up laws unjustly. I guess you could also say it's Hell for claustrophobic folks.",
                            "Nihil"    :"Nihil was the kind of Hell that wasn't really supposed to exist, kinda airy and cold relative to some others. Stories said it was a kind of proto-Hell, split off from someplace in the Heavens... But demons lie, so the truth is hard to figure.",
                            "Acheron"  :"In case you were wondering Acheron is pronounced \"Akkeron\". I know, we learn somethin' new every day. Wishful thinkin' maybe, but if we'd dealt different with them infernal cogwheels here, maybe our ride wouldn't have been so rough...",
                            "Sheol"    :"Sheol ain't like any other Hell. All the others are made for suffering, but Sheol's sort of ground zero for it all. The Red Judge watches over everything from her throne here, waiting for the Unknown, and Heaven's watching. Plus through a quirk of design, it's also the last bulwark separating Heaven from Hell."
}
BASE_OFFSET:str = "0.06"

#codes for the different types of songs
NOACTBANKCODE:str = "{95972dee-fd3a-4a5c-9024-8f714883936e}"

#key is the song name
#list is the following: bank file, bank code, bpm, offset, [preview file, preview start time, preview duration], Artist
SONG_DICT:dict[list[str]] = {}

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
            with open(FILE_NAME, "r") as file:
                display_message_text(attach_outcome_label,2,f"Failed in {(time.time() - start_time):.2f}s because the loader is already attached!", FAILED_COLOR)
                attachment_text[0] = "already attached"
                return
        except Exception as e:
            os.rename(DEACTIVATED_FILE_NAME, FILE_NAME)
            display_message_text(attach_outcome_label,2,f"Successfully Attached in {(time.time() - start_time):.2f}s!", SUCCESS_COLOR)
            attachment_text[0] = "attached"
    except Exception as e:
        display_message_text(attach_outcome_label,6,f"Failed in {(time.time() - start_time):.2f}s with error \"{e}\"!", FAILED_COLOR)
        attachment_text[0] = "attach error"

#Deattaches the customsongs.json file from Hellsinger by renaming the file
#This is so vanila songs can be played without resetting the game
def deattach_script():
    start_time = time.time()
    try:
        try:
            with open(DEACTIVATED_FILE_NAME, "r") as file:
                display_message_text(attach_outcome_label,2,f"Failed in {(time.time() - start_time):.2f}s because the loader is already detached!", FAILED_COLOR)
                attachment_text[0] = "already deattached"
                return
        except Exception as e:
            os.rename(FILE_NAME, DEACTIVATED_FILE_NAME)
            display_message_text(attach_outcome_label,2,f"Successfully Detached in {(time.time() - start_time):.2f}s!", SUCCESS_COLOR)
            attachment_text[0] = "deattached"
    except Exception as e:
        display_message_text(attach_outcome_label,6,f"Failed in {(time.time() - start_time):.2f}s with error \"{e}\"!", FAILED_COLOR)
        attachment_text[0] = "deattach error"

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
        if auto_preview_song.get():
            preview_song()

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
        if chosen_level_config[0] == "Sheol":
            display_message_text(loaded_label, 3, f"Good Luck", "#690000")
        else:
            display_message_text(loaded_label, 3, f"Loaded Song \"{chosen_level_config[1]}\" into Hell \"{chosen_level_config[0]}\" in {time_end-time_start:.2f} seconds!", SUCCESS_COLOR)
    except Exception as e:
        time_end = time.time()
        try:
            with open(DEACTIVATED_FILE_NAME, "r") as file:
                display_message_text(loaded_label, 5, f"Failed load in {time_end - time_start:.2f}s because the script is not attached!", FAILED_COLOR)
                return
        except:
            display_message_text(loaded_label, 10, f"Failed load in {time_end-time_start:.2f}s with error \"{e}\"", FAILED_COLOR)
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
    #set_volume(preview_volume_slider.get())
    fade_thread = threading.Thread(target=_fade_music_in)
    fade_thread.start()
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

def _fade_music_in():
    audio_mult = 0
    while audio_mult < 1.1:
        pygame.mixer.music.set_volume(float(preview_volume_slider.get()/100) * audio_mult)
        time.sleep(0.1)
        audio_mult += 0.1

def set_volume(volume):
    try:
        pygame.mixer.music.set_volume(float(volume)/100)
    except:
        pass

def update_song_stats():
    song = SONG_DICT.get(chosen_level_config[1])
    bpm = song[LIST_SONG_BPM]
    bpm_color:str = ""
    text_size:int = 11
    background:str = BACKGROUND_COLOR
    if int(bpm) < 100:
        bpm_color = "#0abfa7"
    elif int(bpm) < 120:
        bpm_color = "#00a624"
    elif int(bpm) < 140:
        bpm_color = "#59a600"
    elif int(bpm) < 160:
        bpm_color = "#bbc200"
    elif int(bpm) < 180:
        bpm_color = "#faa60a"
    elif int(bpm) < 200:
        bpm_color = "#e34202"
        text_size = 13
    else:
        bpm_color = "#ff0000"
        text_size = 16
        background = "#590000"
        

    song_BPM_label.config(text=f"BPM: {bpm}", fg=bpm_color, font=("Helvetica", text_size), bg=background)
    song_artist_label.config(text=f"Author: {song[LIST_SONG_ARTIST]}")

def update_hell_stats():
    hell=chosen_level_config[0]
    hell_name_label.config(text=hell)
    hell_description_text_label.config(text=HELL_DESCRIPTION.get(hell))

def display_message_text(label:tk.Label, duration:float, message:str, text_color:str = "black"):
    thread = threading.Thread(target=_actually_display_label, args=(label,duration,message,text_color))
    thread.start()

def _actually_display_label(label:tk.Label, duration:float, message:str, text_color:str):
    label.config(text=message,fg=text_color) 
    time.sleep(duration)
    label.config(text="",fg="black")

def fetch_custom_songs():
    song_count = 0
    time_start = time.time()
    with open(CUSTOM_SONGS_FILE_LOCATION, "r") as file:
        all_songs_loaded = False
        file_text = file.read()
        #pulls out a single line from the text file, using ';' tokens to seperate dictionary entries
        start_index = 0
        end_index = 0
        while not all_songs_loaded:
            line:str = ""
            while line == "":
                if file_text[end_index:end_index+1] == "|":
                    line = file_text[start_index:end_index + 1]
                    start_index = end_index
                elif end_index > len(file_text):
                    all_songs_loaded = True
                    break
                else:
                    end_index += 1
            if all_songs_loaded:
                break
            end_index += 1
            start_index = end_index
            #get the information we need from that line

            start_and_stop = [0, 0]
            key = _fetch_word(start_and_stop, line)
            bank_file_name = _fetch_word(start_and_stop, line)
            bank_code = _fetch_word(start_and_stop, line)
            bpm = _fetch_word(start_and_stop, line)
            offset = _fetch_word(start_and_stop, line)
            preview_stuff:list = [_fetch_word(start_and_stop, line), int(_fetch_word(start_and_stop, line)), int(_fetch_word(start_and_stop, line))]
            artist = _fetch_word(start_and_stop, line)
            
            SONG_DICT.update({key:[bank_file_name,bank_code,bpm,offset,preview_stuff,artist]})
            song_count += 1
    print(f"Loaded {song_count} songs in {time.time() - time_start} seconds")

def _fetch_word(start_and_stop:list[int], line:str) -> str:
    line_end = start_and_stop[1]
    line_start = start_and_stop[0]
    return_str = ""
    while return_str == "":
        if line[line_end : line_end + 1] == "," or line[line_end : line_end + 1] == "|":
            return_str = line[line_start:line_end]
            if return_str == "NOACTBANKCODE":
                return_str = NOACTBANKCODE
            if return_str == "BASE_OFFSET":
                return_str = BASE_OFFSET
        else:
            line_end += 1
    start_and_stop[1] = line_end + 1
    start_and_stop[0] = line_end + 1
    return return_str


fetch_custom_songs()

#root setup
root = tk.Tk()
root.title("MH Custom Song Loader")
root.geometry("700x420")
root.resizable(False,False)
root.iconphoto(False,tk.PhotoImage(file="Icon.png"))
root.wm_attributes("-topmost", 1)
root.config(bg=BACKGROUND_COLOR)

#Labels
label = tk.Label(root, text="METAL HELLSINGER CUSTOM SONG LOADER", font=("Helvetica", 22), bg=BACKGROUND_COLOR, fg="#ff4000")
label.pack(side=tk.TOP)
hell_label = tk.Label(root,text="HELL", font=("Helvetica", 18), bg=BACKGROUND_COLOR, fg="#c90000")
song_label = tk.Label(root,text="SONG", font=("Helvetica", 18), bg=BACKGROUND_COLOR, fg="#c90000")
song_options_label = tk.Label(root, text="SONG OPTIONS", font=("Helvetica", 14), bg=BACKGROUND_COLOR,fg="#c90000")
song_stats_label = tk.Label(root, text="SONG STATS", font=("Helvetica", 14), bg=BACKGROUND_COLOR,fg="#c90000")
song_BPM_label = tk.Label(root, text="BPM: n/a", bg=BACKGROUND_COLOR,fg="#ff602b",font=("Helvetica",11))
song_artist_label = tk.Label(root, text="Author: n/a", bg=BACKGROUND_COLOR,fg="#ff602b", font=("Helvetica",11))
hell_name_label = tk.Label(root, text="n/a", font=("Helvetica", 30), anchor="center", bg=BACKGROUND_COLOR,fg="#ff0000")
hell_description_text_label = tk.Label(root, text="n/a",wraplength=350, bg=BACKGROUND_COLOR, fg="#de0000", font=("Helvetica",14))
volume_slider_label = tk.Label(root, text="Volume", font=("Helvetica", 7),bg=BACKGROUND_COLOR, fg="#ff602b")
attach_outcome_label = tk.Label(root, text="",bg=BACKGROUND_COLOR) #dont change color
loaded_label = tk.Label(root, text="", font=("Helvetica", 11),fg="green",bg=BACKGROUND_COLOR) #dont change color

#Buttons
attach_script_button = tk.Button(root,text="Attach", command=lambda:attach_script(),bg="#380000", fg="#d40000")
deattach_script_button = tk.Button(root, text="Detach", command=lambda:deattach_script(), bg="#380000", fg = "#d40000")
load_song_button = tk.Button(root, text="LOAD", font=("Helvetica", 30), width=100, command=lambda:load_level_without_prompts(), bg="#610000", fg="#ff4000")
preview_button = tk.Button(root, text="Preview", command=lambda:preview_song(), bg="#380000", fg="#d40000",width = 8, font=("Helvetica", 12))
stop_preview_button = tk.Button(root, text="Stop", command=lambda:stop_preview(), bg="#380000", fg="#d40000", width=8, font=("Helvetica", 12))

#dropdowns
#songs
selected_song = StringVar(root)
selected_song.set(list(SONG_DICT.keys())[0])
song_select_dropdown = tk.OptionMenu(root, selected_song, *SONG_DICT.keys(), command=on_select)
song_select_dropdown.config(bg="#380000", fg="#fa3605", height=1, font=("Helvetica", 12))
#hells
selected_hell = StringVar(root)
selected_hell.set(list(HELL_LIST)[0])
hell_select_dropdown = tk.OptionMenu(root, selected_hell, *HELL_LIST, command=on_select)
hell_select_dropdown.config(bg="#380000", fg="#fa3605", height=1, font=("Helvetica", 12))
#preview volume slider
preview_volume_slider = tk.Scale(root, from_=100, to=0,orient="vertical",command=set_volume,width=12, length=100,bg="#380000",fg="#ff602b",font=("Helvetica", 12))

#checkbox
auto_preview_song = tk.BooleanVar()
auto_preview_song_checkbox = tk.Checkbutton(root, text="Autoplay", variable=auto_preview_song, onvalue=True, offvalue=False, bg=BACKGROUND_COLOR,fg="#ff602b")
#positioning

load_song_button.pack(side=tk.BOTTOM)
attach_outcome_label.place(x=100,y=38)

#top
attach_script_button.place(x=3,y=36)
deattach_script_button.place(x=53,y=36)

#left
hell_label.place(x=0,y=100)
hell_select_dropdown.place(x=0,y=130)
song_label.place(x=0, y=200)
song_select_dropdown.place(x=0,y=230)

#right
song_options_label.place(x=545,y=58)
preview_button.place(x=612,y=129)
stop_preview_button.place(x=612,y=170)
preview_volume_slider.set(25)
preview_volume_slider.place(x=552,y=97)
volume_slider_label.place(x=557, y=80)
auto_preview_song_checkbox.place(x=612,y=97)

song_stats_label.place(x=545,y=220)
song_artist_label.place(x=545, y=250)
song_BPM_label.place(x=545, y=270)

#center
hell_name_label.place(x=265,y=75)
loaded_label.pack(side=tk.BOTTOM)
hell_description_text_label.place(x=160,y=130)

chosen_level_config = [HELL_LIST[0], list(SONG_DICT.keys())[0]]
playing_preview_song = [""]
attachment_text:list[str] = [""]

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
