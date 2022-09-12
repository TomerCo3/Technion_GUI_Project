from tkinter import filedialog
import sounddevice as sd
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import ttk
import tkinter as tk
import queue
import soundfile as sf
import threading
from tkinter import messagebox
import os
import shutil


# functions for getting the user name and files path
def getDirectory():
        # get a directory path by user
        global directory_path
        directory_path = filedialog.askdirectory(title="Dialog box")
        print(directory_path)
        global sentences_folder
        sentences_folder = os.listdir(directory_path)
        for sen in sentences_folder:
            if not sen.endswith('.txt'):
                sentences_folder.remove(sen)
        global sentence_file_name
        sentence_file_name = sentences_folder[0]
        global sentence
        sentences_folder.remove(sentence_file_name)
        sentence = open(os.path.join(directory_path, sentence_file_name)).read()
        global filename
        filename = sentence_file_name.replace('.txt', '.wav')


def getUserName():
        global user_name
        user_name = e.get()
        try: # first time using the name
            global users_path
            users_path = os.path.join(base_path, user_name)
            curr_names_folder = os.mkdir(users_path)
        except: # the name is already used
            def popup_win():
                # wants to enter a new name
                def enter_new_name():
                    e.delete(0, END)
                    top1.destroy()  
                # continue with a differant name
                def continue_with_name():
                    def exit_button():
                        top2.destroy()
                        top2.update()
                    top1.destroy()
                    global users_path
                    users_path = os.path.join(base_path, user_name)

                    top2 = Toplevel()
                    label2 = tk.Label(top2, text="Great! press start on the buttom of the main page and continue recording the sentences after that press the continue button to continue")
                    exit_btn = tk.Button(top2, text="Exit", command=exit_button)
                    label2.pack()
                    exit_btn.pack()

                top1 = Toplevel()
                label1 = tk.Label(top1, text="Name already in use, do you want to continue with the name given or enter a differant one?")
                continue_btn = tk.Button(top1, text="Continue", command=continue_with_name)
                newName_btn = tk.Button(top1, text="Enter a new name", command=enter_new_name)

                label1.grid(row=1, column=0)
                continue_btn.grid(row=2, column=0)
                newName_btn.grid(row=2, column=1)
            popup_win()
                


# functions for recording and displaying the sentences
def start_recording():
        #If recording is selected, then the thread is activated
        t1=threading.Thread(target=record_audio)
        t1.start()
def stop_recording():
    #To stop, set the flag to false
    global recording
    recording = False
    messagebox.showinfo(message="Recording finished")
def play_recording():
    #To play a recording, it must exist.
    if file_exists:
        #Read the recording if it exists and play it
        data, fs = sf.read(filename, dtype='float32')
        sd.play(data,fs)
        sd.wait()
    else:
        #Display and error if none is found
        messagebox.showerror(message="Record something to play")

#Fit data into queue
def callback(indata, frames, time, status):
    q.put(indata.copy())

#Recording function
def record_audio(): 
    #Declare global variables   
    global recording
    #Set to True to record
    recording= True  
    global file_exists
    #Create a file to save the audio
    messagebox.showinfo(message="Recording Audio. Speak into the mic")
    with sf.SoundFile(filename, mode='w', samplerate=44100,
                        channels=1) as file:
    #Create an input stream to record audio without a preset time
        with sd.InputStream(samplerate=44100, channels=1, callback=callback):
            while recording == True:
                #Set the variable to True to allow playing the audio later
                file_exists =True
                #write into file
                file.write(q.get())

def record_again():
    os.remove(os.path.join(users_path, filename))
    start_recording()

def main_window():
    global base_path
    base_path = '/Users/tomer/tk_voice_recorder'
    
    #Functions to play, stop and record audio in Python voice recorder
    #The recording is done as a thread to prevent it being the main process
    
    #Define the user interface for Voice Recorder using Python
    voice_rec = Tk()

    def continue_func():
        if T.get('1.0', 'end-1c') == "Hello, please type in your full name and choose the directory you will be working with, then press continue":
            sentence_file_name = sentences_folder[0]
            sentences_folder.remove(sentence_file_name)
            global sentence_path
            sentence_path = os.path.join(directory_path, sentence_file_name)
            sentence = open(sentence_path).read()
            T.delete("1.0", "end")
            T.insert(tk.END, sentence)
            global filename
            filename = sentence_file_name.replace('.txt', '.wav')
            voice_rec.update()
        else:
            try:
                shutil.copy(sentence_path, users_path)
                voice_file_path = os.path.join(base_path, filename)
                shutil.move(voice_file_path, users_path)
            except:
                def popup_window():
                    def update_voice_file():
                        old_voice_file = os.path.join(users_path, filename)
                        os.remove(old_voice_file)
                        voice_file_path = os.path.join(base_path, filename)
                        shutil.move(voice_file_path, users_path)
                        top.destroy()
                    
                    def remain_with_old_file():
                        os.remove(sentence_path)
                        top.destroy()

                    top = Toplevel()
                    label = tk.Label(top, text="Already recorder the sentence, do you want to update to the new file or remain with the old one and delete the new?")
                    update_btn = tk.Button(top, text="Update", command=update_voice_file)
                    remain_with_old_btn = tk.Button(top, text="Stay with old file", command=remain_with_old_file)
                    label.pack()
                    update_btn.pack()
                    remain_with_old_btn.pack()
                popup_window()

            sentence_file_name = sentences_folder[0]
            sentences_folder.remove(sentence_file_name)
            sentence_path = os.path.join(directory_path, sentence_file_name)
            sentence = open(sentence_path).read()
            T.delete("1.0", "end")
            T.insert(tk.END, sentence)
            filename = sentence_file_name.replace('.txt', '.wav')
            voice_rec.update()
           


    global q
    #Create a queue to contain the audio data
    q = queue.Queue()
    #Declare variables and initialise them
    recording = False
    file_exists = False

    name_text = tk.Text(voice_rec, width=15, height=1, font=('Ariel', 14))
    name_text.insert(tk.END, "Enter your full name:")
    directory_text = tk.Text(voice_rec, width=33, height=1, font=('Ariel', 14))
    directory_text.insert(1.0, "Select the directory you will be working with:")
    # text to get the users name
    global e
    e = tk.Entry(voice_rec)
    e.focus_set()

    okay_btn = tk.Button(voice_rec, text='Submit Name', command=getUserName)
    dialog_btn = tk.Button(voice_rec, text='Select Directory', command=getDirectory)

    name_text.grid(row=1, column=0)
    e.grid(row=1, column=1)
    okay_btn.grid(row=1, column=2)
    directory_text.grid(row=2, column=0)
    dialog_btn.grid(row=2, column=1)

    # spacers to make space between top of the window to the buttom
    spacer1 = tk.Label(voice_rec, text="")
    spacer2 = tk.Label(voice_rec, text="")
    spacer3 = tk.Label(voice_rec, text="")
    spacer4 = tk.Label(voice_rec, text="")
    #grid the spacers
    spacer1.grid(row=3, column=0)
    spacer2.grid(row=4, column=0)
    spacer3.grid(row=5, column=0)
    spacer4.grid(row=6, column=0)

    #Progress Bar
    bar = Progressbar(voice_rec, length=400, style='black.Horizontal.TProgressbar')
    bar['value']=70
    #Text
    sentence = "Hello, please type in your full name and choose the directory you will be working with, then press continue"
    global T
    T = Text()
    T.config(font=("Ariel", 20))
    T.insert(tk.END, sentence)
    
    #Button to record audio
    record_btn = Button(voice_rec, width=20, text="Record Audio", command=start_recording)
    stop_btn = Button(voice_rec, width=20, text="Stop Recording", command=stop_recording)
    play_btn = Button(voice_rec, width=20, text="Play Recording", command=play_recording)
    record_again_btn = Button(voice_rec, text="Record Again", command=record_again) 
    continue_btn = Button(voice_rec, text="Continue", command=continue_func)
    quit_btn = Button(voice_rec, text="Quit", command=voice_rec.destroy)
    
    record_btn.grid(row=7,column=0)
    stop_btn.grid(row=7,column=1)
    play_btn.grid(row=7,column=2)
    record_again_btn.grid(row=7, column=3)
    bar.grid(row=8, column=0, columnspan=3)
    T.grid(row=9, column=0, columnspan=4)
    continue_btn.grid(row=11, column=0)
    quit_btn.grid(row=11, column=1)
    voice_rec.attributes('-fullscreen', True)
    voice_rec.mainloop()

main_window()