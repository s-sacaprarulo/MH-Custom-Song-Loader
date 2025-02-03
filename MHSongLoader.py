import os
import tkinter as tk
from tkinter import StringVar
from tkinter import messagebox
import time
import pygame
import threading
import copy


#TODO: The stuff we need to make before making this project public
# Add a way to set where Config.txt is
# Add a way to change/set where the Custom_Song_List.txt file is
# Add a way to import a song without Author or Preview stuff because they arent essential


SETTINGS_CUSTOM_SONG_FILE_LOCATION_OPTION = "Custom Song List Location"
SELECTED_PROFILE_SETTINGS_DICT_OPTION = "Selected Profile"

JSON_FILE_LOCATION:str = ""
FILE_NAME:str =  ""
DEACTIVATED_FILE_NAME:str = ""

# file location, inactive file location
FILE_LOCATION_PROFILES:dict[list[str]] = {}

CUSTOM_SONGS_FILE_LOCATION:str = "Custom_Song_List.txt"
SETTINGS_FILE_LOCATION = "Config.txt"
SETTINGS_VOLUME_OPTION = "Volume"

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

CONFIG_TEXT_FILE_TEXT = '''Text written in braces are read by the program.
"|" tokens are used to separate entries, and all entries should end with a "|" token before the close bracket token token IE Setting|entry|
It is suggested you do not modify this file unless you know what you are doing.
CASE SENSITIVE BY THE WAY

obviously, because I can write, I will try to describe everything in as much detail as I can if you do want to edit this file for some reason.


GENERAL SETTINGS

The location that the program stores all your custom songs to.
<Custom Song List Location|Custom_Song_List.txt|> 

The currently selected profile. The program reads and (will eventually) make the second part be on the dropdown by default
<Selected Profile|TEST|>

The volume that the volume slider starts at
<Volume|29|>


PROFILES

Profiles follow the following format:
Profile being the Setting option
The first entry after that is the profile name
The entry after that is the file location for that profile'''

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

#these are pulled at the start of the program from the CUSTOM_SONGS_FILE_LOCATION text file in the FETCH_CUSTOM_SONGS fucntion
#key is the song name
#list is the following: bank file, bank code, bpm, offset, [preview file, preview start time, preview duration], Artist
SONG_DICT:dict[list[str]] = {}
SETTINGS_DICT:dict[str] = {}
PROFILE_DICT:dict[list[str]] = {}

preview_song_index = 0

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
    pygame.mixer.music.set_volume(0) #NOTE: I changed this and couldn't test it, this may break the sound mixer
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
    global preview_song_index
    preview_song_index += 1
    last_index = preview_song_index
    time.sleep(song_durr)
    if (preview_song_index == last_index):
        pygame.mixer.music.stop()
#makes the music fade in when you start previewing a file
def _fade_music_in():
    audio_mult = 0
    while audio_mult < 1.1:
        pygame.mixer.music.set_volume(float(preview_volume_slider.get()/100) * audio_mult)
        time.sleep(0.1)
        audio_mult += 0.1

#sets the volume of the volume mixer to whatever the volume slider says on the window. This executes after changing the volume slider
def set_volume(volume):
    try:
        pygame.mixer.music.set_volume(float(volume)/100)
    except:
        pass
    finally:
        change_an_option_in_config(SETTINGS_VOLUME_OPTION, volume)

#changes the stats for the song whenever you change something in the song select dropdown or upload a new song. IE the song changes
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

#changes the description of the hell whenever a new Hell is chosen
def update_hell_stats():
    hell=chosen_level_config[0]
    hell_name_label.config(text=hell)
    hell_description_text_label.config(text=HELL_DESCRIPTION.get(hell))

#makes a textbox display a message on a textbox for a certain amount of time
def display_message_text(label:tk.Label, duration:float, message:str, text_color:str = "black"):
    thread = threading.Thread(target=_actually_display_label, args=(label,duration,message,text_color))
    thread.start()
def _actually_display_label(label:tk.Label, duration:float, message:str, text_color:str):
    label.config(text=message,fg=text_color) 
    time.sleep(duration)
    label.config(text="",fg="black")

#looks to the custom_song_list file and pulls custom songs from that and adds them to the SONG_DICT dictionary
def fetch_custom_songs() -> int:
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
    return song_count
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

#makes the window always appear on top if that checkbox is ticked
def set_always_on_top():
    if always_on_top.get():
        root.wm_attributes("-topmost", True)
    else:
        root.wm_attributes("-topmost", False)

#creates a new window for creating a new song
def create_new_song():
    new_song_window = tk.Tk()
    new_song_window.title("NEW SONG")
    new_song_window.geometry("500x320")
    new_song_window.config(bg=BACKGROUND_COLOR)
    new_song_window.wm_attributes("-topmost", True)
    new_song_window.resizable(False,False)

    #left hand stuff (the required stuff)

    window_title_label = tk.Label(new_song_window,text="Create New Song",font=("Helvetica", 22), bg=BACKGROUND_COLOR, fg="#ff4000")
    song_name_tb_label = tk.Label(new_song_window,text="Song Name",bg=BACKGROUND_COLOR,fg="#ff4000")
    song_bankfile_tb_label = tk.Label(new_song_window,text="Bank File (with '.bank')",bg=BACKGROUND_COLOR,fg="#ff4000")
    song_bpm_tb_label = tk.Label(new_song_window,text="Beats Per Minute",bg=BACKGROUND_COLOR,fg="#ff4000")
    song_offset_tb_label = tk.Label(new_song_window,text="BPM offset",bg=BACKGROUND_COLOR,fg="#ff4000")
    song_bankcode_tb_label = tk.Label(new_song_window,text="File Code",bg=BACKGROUND_COLOR,fg="#ff4000")

    song_name_textbox = tk.Text(new_song_window,width=30, height=1)
    song_bankfile_textbox = tk.Text(new_song_window,width=20, height=1)
    song_bpm_textbox = tk.Text(new_song_window,width=20, height=1)
    song_offset_textbox = tk.Text(new_song_window,width=20, height=1)
    song_bankcode_textbox = tk.Text(new_song_window,width=20, height=1)

    window_title_label.pack(side=tk.TOP)
    song_name_tb_label.place(x=130,y=30)
    song_name_textbox.place(x=130, y=50)

    song_bankfile_tb_label.place(x=30,y=80)
    song_bankfile_textbox.place(x=30,y=100)

    song_bankcode_tb_label.place(x=30,y=130)
    song_bankcode_textbox.place(x=30,y=150)

    song_bpm_tb_label.place(x=30,y=180)
    song_bpm_textbox.place(x=30,y=200)

    song_offset_tb_label.place(x=30,y=230)
    song_offset_textbox.place(x=30,y=250)

    #right hand stuff (not-required stuff)
    song_previewfile_tb_label = tk.Label(new_song_window,text="Preview Audio File (with extension)",bg=BACKGROUND_COLOR,fg="#ff4000")
    song_previewstart_tb_label = tk.Label(new_song_window,text="Preview Start time (30 starts 30s in)",bg=BACKGROUND_COLOR,fg="#ff4000")
    song_previewduration_tb_label = tk.Label(new_song_window,text="Preview Duration (15 plays for 15s)",bg=BACKGROUND_COLOR,fg="#ff4000")
    song_artist_tb_label = tk.Label(new_song_window,text="Artist",bg=BACKGROUND_COLOR,fg="#ff4000")

    song_previewfile_textbox = tk.Text(new_song_window,width=20, height=1)
    song_previewstart_textbox = tk.Text(new_song_window,width=20, height=1)
    song_previewduration_textbox = tk.Text(new_song_window,width=20, height=1)
    song_artist_textbox = tk.Text(new_song_window,width=20, height=1)

    song_artist_tb_label.place(x=300,y=80)
    song_artist_textbox.place(x=300,y=100)

    song_previewfile_tb_label.place(x=300,y=130)
    song_previewfile_textbox.place(x=300,y=150)

    song_previewstart_tb_label.place(x=300,y=180)
    song_previewstart_textbox.place(x=300,y=200)

    song_previewduration_tb_label.place(x=300,y=230)
    song_previewduration_textbox.place(x=300,y=250)

    create_button = tk.Button(new_song_window, text="Create Song!", font=("Helvetica", 16), width=100, command=lambda:write_new_song_string_to_file(song_name_textbox.get("1.0", 'end-1c'),song_bankfile_textbox.get("1.0", 'end-1c'),song_bankcode_textbox.get("1.0", 'end-1c'),song_bpm_textbox.get("1.0", 'end-1c'),song_offset_textbox.get("1.0", 'end-1c'),song_previewfile_textbox.get("1.0", 'end-1c'),song_previewstart_textbox.get("1.0", 'end-1c'),song_previewduration_textbox.get("1.0", 'end-1c'),song_artist_textbox.get("1.0", 'end-1c')), bg="#610000", fg="#ff4000")
    create_button.pack(side=tk.BOTTOM)
    new_song_window.mainloop()

#using given parameters, write a SONG_DICT entry to the customsongslist text file and refreshes the SONG_DICT dictionary
def write_new_song_string_to_file(song_name:str, song_file:str,song_code:str,song_bpm:str,song_offset:str,song_prevlocation:str, song_prevstart:str,song_prevdur:str,song_artist:str):
    past_str = ""
    try:
        with open(CUSTOM_SONGS_FILE_LOCATION, "r") as file:
            past_str = file.read()
    except:
        print("No custom song file detected!")
        return

    if song_code == "NOACTBANKCODE":
        song_code = NOACTBANKCODE
    if song_offset == "BASEOFFSET":
        song_offset = BASE_OFFSET

    try:
        check_new_song_failsafes(song_name, song_file,song_code,song_bpm,song_offset,song_prevlocation, song_prevstart,song_prevdur,song_artist)
    except ValueError as e:
        output = messagebox.askyesno("Song Creation Error!", f"Song creation failed because: {e}. You can continue by clicking the \"Yes\" button below.\nWould you like to continue with the creation process?")
        if not output:
            return

    with open(CUSTOM_SONGS_FILE_LOCATION, "w") as file:
        file.write(past_str + f"{song_name},{song_file},{song_code},{song_bpm},{song_offset},{song_prevlocation},{song_prevstart},{song_prevdur},{song_artist}|")
    fetch_custom_songs()
    put_songs_on_dropdown()
    messagebox.showinfo("MHSong Loader", f"New song \"{song_name}\" successfully written to file \"{CUSTOM_SONGS_FILE_LOCATION}\" and loaded into custom song loader.")

#puts songs on dropdown by destroying the previous one    
def put_songs_on_dropdown():
    try:
        song_dropdown[0].destroy()
        song_dropdown.pop(0)
    except:
        pass
    selected_song = StringVar(root)
    selected_song.set(list(SONG_DICT.keys())[0])
    song_select_dropdown = tk.OptionMenu(root, selected_song, *SONG_DICT.keys(), command=on_select)
    song_select_dropdown.config(bg="#380000", fg="#fa3605", height=1, font=("Helvetica", 12))
    song_select_dropdown.place(x=0,y=230)
    song_dropdown.append(song_select_dropdown)
    chosen_level_config[1] = list(SONG_DICT.keys())[0]
    time_start = time.time()
    update_song_stats()
    display_message_text(loaded_label,5, f"Loaded {song_count} songs in {time.time() - time_start:.3f} seconds", SUCCESS_COLOR)


def check_new_song_failsafes(song_name:str, song_file:str,song_code:str,song_bpm:str,song_offset:str,song_prevlocation:str, song_prevstart:str,song_prevdur:str,song_artist:str):
    #A song cannot be loaded if 
    #-ANY part of the song contains a ',' or '|' token
    #-The songbpm, offset, previewstart, or or prevduration, except if song_offset is "BASE OFFSET"
    #-Song_file does not end in '.bank'
    #-Song_prev file must end in '.wav', '.mp3', or '.ogg'. Technically this is not required, but the extension is required, and these are the most common
    if "," in song_name or "|" in song_name or "," in song_file or "|" in song_file or "," in song_code or "|" in song_code or "," in song_bpm or "|" in song_bpm or "," in song_offset or "|" in song_offset or "," in song_prevlocation or "|" in song_prevlocation or "," in song_prevstart or "|" in song_prevstart or "," in song_prevdur or "|" in song_prevdur or "," in song_artist or "|" in song_artist:
        raise ValueError("Input cannot contain the \"|\" or \",\" tokens")
    try:
        float(song_bpm)
        float(song_offset)
        float(song_prevstart)
        float(song_prevdur)
    except:
        raise ValueError("The song's BPM, Offset, preview start time, and/or start duration must be only numbers")
    if ".bank" not in song_file:
        raise ValueError("The song file does not contain \".bank\"")

def get_settings():
    # gets the file locations from the config.txt file
    # reads through the file to do so, only reading text in <> tokens
    
    #Failsafe
    try:
        with open(SETTINGS_FILE_LOCATION, "r") as file:
            file.read()
    except:
        no_config_text_file_failsafe()
    
    all_settings_pulled = False

    with open(SETTINGS_FILE_LOCATION, "r") as file:
        file_text = file.read()
        if len(file_text) == 0:
            messagebox.askyesnocancel("MH Custom Song Loader", "The found Config.txt file has been detected as blank. This may have happened due to a program crash, file corruption, or maunally changing the file. The program can attempt to put in the essential text to the file. \n Press yes to add the essential text. Press no to ignore this message (NOT RECOMMENDED). Press Cancel to close the prgoram")
        start_index = 0
        end_index = 0
        while not all_settings_pulled:
            line:str = ""
            while line == "":
                if file_text[end_index:end_index+1] == "<":
                    bracket_start_index = end_index + 1
                    while line == "":
                        if file_text[end_index:end_index+1] == ">":
                            line = file_text[bracket_start_index:end_index]
                            start_index = end_index
                        elif end_index > len(file_text):
                            all_settings_pulled = True
                            break
                        else:
                            end_index += 1
                elif end_index > len(file_text):
                    all_settings_pulled = True
                    break
                else:
                    end_index += 1
                    start_index += 1
            if all_settings_pulled:
                break
            end_index += 1
            start_index = end_index

            start_and_stop = [0, 0]
            setting = _fetch_word(start_and_stop, line)
            if setting == "Profile":
                profile_name = _fetch_word(start_and_stop, line)
                profile_location = _fetch_word(start_and_stop, line)
                #to make the inactivee file, we need to go back through the string until we past the ".json". then we will add something there.
                to_be_inactive_location = copy.deepcopy(profile_location)
                inactive_file_location = ""
                made_inactive = False
                part = len(to_be_inactive_location)
                while not made_inactive:
                    letter = to_be_inactive_location[part-1:part]
                    if letter == ".":
                        inactive_file_location = profile_location[0:part-1] + "_Inactive" + profile_location[part - 1:len(to_be_inactive_location)]
                        made_inactive = True
                    elif part < 0:
                        raise NameError("Could not find a \".\" token in the file location")
                    else:
                        part -= 1
                PROFILE_DICT.update({profile_name:[profile_location, inactive_file_location]})
                continue
            option = _fetch_word(start_and_stop, line)
            SETTINGS_DICT.update({setting:option})   
def set_file_locations():
    global CUSTOM_SONGS_FILE_LOCATION
    CUSTOM_SONGS_FILE_LOCATION = SETTINGS_DICT.get(SETTINGS_CUSTOM_SONG_FILE_LOCATION_OPTION)
    profile = SETTINGS_DICT.get(SELECTED_PROFILE_SETTINGS_DICT_OPTION)
    try:
        global FILE_NAME
        FILE_NAME = PROFILE_DICT.get(profile)[0]
        global JSON_FILE_LOCATION
        JSON_FILE_LOCATION = PROFILE_DICT.get(profile)[0]
        global DEACTIVATED_FILE_NAME
        DEACTIVATED_FILE_NAME = PROFILE_DICT.get(profile)[1]
    except:
        pass
def change_an_option_in_config(changing_option, new_value):
    #we are finding the profile we need to change
    start = 0
    changing_file_start = 0
    changing_file_end = 0
    end = 0
    try:
        with open(SETTINGS_FILE_LOCATION, "r") as file:
            file.read()
    except:
        raise FileExistsError("Could not find a settings file!")
    
    all_settings_pulled = False

    with open(SETTINGS_FILE_LOCATION, "r") as file:
        file_text = file.read()
        end = len(file_text)
        start_index = 0
        end_index = 0
        modifying_line_start = 0
        #find a setting
        while not all_settings_pulled:
            line:str = ""
            while line == "":
                if file_text[end_index:end_index+1] == "<":
                    modifying_line_start = end_index
                    bracket_start_index = end_index + 1
                    while line == "":
                        if file_text[end_index:end_index+1] == ">":
                            line = file_text[bracket_start_index:end_index]
                            start_index = end_index
                        elif end_index > len(file_text):
                            all_settings_pulled = True
                            break
                        else:
                            end_index += 1
                elif end_index > len(file_text):
                    all_settings_pulled = True
                    break
                else:
                    end_index += 1
                    start_index += 1
            if all_settings_pulled:
                break
            end_index += 1
            start_index = end_index
            #check if its the setting we want
            start_and_stop = [0, 0]
            found_setting = _fetch_word(start_and_stop, line)
            if found_setting == changing_option:
                #if it is
                #i dont have time so im gonna pseudocode
                #continue going in the config text until the next '|' token
                #continue running through the rest of the config.txt
                #when we reach the end, change both changing_file_end and end to be the values they should be
                #make the text file equal the text before changing_file_start, then the correct profile, then a "|" token, then the rest of the text
                found_next_line = False
                end_index = modifying_line_start
                while not found_next_line:
                    if file_text[end_index:end_index + 1] == "|":
                        found_next_line = True
                    elif end_index > end:
                        raise IndexError("Reached the end of the text file before finding a | token. Check the config text file")
                    else:
                        end_index += 1
                changing_file_start = end_index
                end_index += 1
                found_next_line = False
                while not found_next_line:
                    if file_text[end_index:end_index + 1] == "|":
                        found_next_line = True
                    elif end_index > end:
                        raise IndexError("Reached the end of the text file before finding a | token. Check the config text file")
                    else:
                        end_index += 1
                changing_file_end = end_index
                with open(SETTINGS_FILE_LOCATION, "w") as editing_file:
                    before_modification_str = file_text[start:changing_file_start]
                    after_modification_str = file_text[changing_file_end:end]
                    editing_file.write(before_modification_str + "|" + new_value + after_modification_str)
                    return
def change_profile(profile):
    change_an_option_in_config(SELECTED_PROFILE_SETTINGS_DICT_OPTION, profile)
    global PROFILE_DICT
    PROFILE_DICT = {}
    get_settings()
    set_file_locations()

def no_config_text_file_failsafe():
    create_the_file = messagebox.askyesno("MH Custom Song Loader ERROR", "Could not find a Config.txt file. The program will not function without this essential file. It has either been renamed or deleted. The program can attempt to make a file at it's directory. Alternatively, you can create one yourself. Clicking \"yes\" will attempt to create the file.")
    if create_the_file:
        with open("Config.txt", "x") as file:
            file.write(CONFIG_TEXT_FILE_TEXT)
    else:
        exit()

start_time = time.time()
get_settings()
set_file_locations()
song_count = fetch_custom_songs()

#root setup
root = tk.Tk()
root.title("MH Custom Song Loader")
root.geometry("700x420")
root.resizable(False,False)
root.iconphoto(False,tk.PhotoImage(file="Icon.png"))
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
create_new_song_button = tk.Button(root, text="NEW", command=lambda:create_new_song(), bg="#380000", fg="#d40000", width=8, font=("Helvetica", 12))

#dropdowns
#songs
song_dropdown:list[tk.OptionMenu] = []
#hells
selected_hell = StringVar(root)
selected_hell.set(list(HELL_LIST)[0])
hell_select_dropdown = tk.OptionMenu(root, selected_hell, *HELL_LIST, command=on_select)
hell_select_dropdown.config(bg="#380000", fg="#fa3605", height=1, font=("Helvetica", 12))
#file location profile
selected_profile = StringVar(root)
selected_profile.set(SETTINGS_DICT.get(SELECTED_PROFILE_SETTINGS_DICT_OPTION)) #TODO: Make the program read the file and set the currently active profile to be on the dropdown at startup
profile_select_dropdown = tk.OptionMenu(root, selected_profile, *PROFILE_DICT.keys(), command=change_profile)
profile_select_dropdown.config(bg="#380000", fg="#fa3605", height=1, font=("Helvetica", 12))

#preview volume slider
preview_volume_slider = tk.Scale(root, from_=100, to=0,orient="vertical",command=set_volume,width=12, length=100,bg="#380000",fg="#ff602b",font=("Helvetica", 12))

#checkbox
auto_preview_song = tk.BooleanVar()
auto_preview_song_checkbox = tk.Checkbutton(root, text="Autoplay", variable=auto_preview_song, onvalue=True, offvalue=False, bg=BACKGROUND_COLOR,fg="#ff602b")
always_on_top = tk.BooleanVar()
always_on_top_checkbox = tk.Checkbutton(root, text="Always on top", variable = always_on_top, onvalue=True, offvalue=False, bg=BACKGROUND_COLOR,fg="#ff602b",command=set_always_on_top)
#positioning

load_song_button.pack(side=tk.BOTTOM)
attach_outcome_label.place(x=100,y=38)
profile_select_dropdown.place(x=0,y=305)

#top
attach_script_button.place(x=3,y=36)
deattach_script_button.place(x=53,y=36)
always_on_top_checkbox.place(x=0,y=65)

#left
hell_label.place(x=0,y=100)
hell_select_dropdown.place(x=0,y=130)
song_label.place(x=0, y=200)


#right
song_options_label.place(x=545,y=58)
preview_button.place(x=612,y=129)
stop_preview_button.place(x=612,y=170)
preview_volume_slider.set(SETTINGS_DICT.get(SETTINGS_VOLUME_OPTION))
preview_volume_slider.place(x=552,y=97)
volume_slider_label.place(x=557, y=80)
auto_preview_song_checkbox.place(x=612,y=97)

song_stats_label.place(x=545,y=220)
song_artist_label.place(x=545, y=250)
song_BPM_label.place(x=545, y=270)

#center
hell_name_label.place(x=265,y=75)
hell_description_text_label.place(x=160,y=130)

create_new_song_button.place(x=615,y=307)

loaded_label.pack(side=tk.BOTTOM)
chosen_level_config = [HELL_LIST[0], list(SONG_DICT.keys())[0]]
playing_preview_song = [""]
attachment_text:list[str] = [""]

put_songs_on_dropdown()
update_hell_stats()
display_message_text(loaded_label, 5, f"Loaded {song_count} songs in {time.time() - start_time:.3f} seconds", SUCCESS_COLOR)
root.mainloop()