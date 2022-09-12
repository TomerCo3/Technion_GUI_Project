import shutil
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


def starting_window():
    def directory():
        # get a directory path by user
        global filepath
        filepath=filedialog.askdirectory(title="Dialog box")
        print(filepath)
        return filepath

    def printText():
        global user_name
        user_name = e.get()
        print(user_name)
        return user_name

    global starting_win
    starting_win = Tk()
    starting_win.geometry('400x200')

    e = tk.Entry(starting_win)
    e.grid(row=1, column=0)
    e.focus_set()

    global curr_name
    global curr_dir
    global base_path

    curr_name = ''
    curr_dir = ''

    base_path = '/Users/tomer/tk_voice_recorder'

    okay_btn = tk.Button(starting_win, text='Submit Name', command = lambda: curr_name==printText())
    dialog_btn = tk.Button(starting_win, text='Select Directory', command = lambda: curr_dir==directory())
    next_btn = tk.Button(starting_win, text='Next', command=main_window)
    exit_btn = tk.Button(starting_win, text='Done', command=exit)

    okay_btn.grid(row=1, column=1)
    dialog_btn.grid(row=2, column=0)
    next_btn.grid(row=3, column=0)
    exit_btn.grid(row=3, column=1)
   
    starting_win.attributes('-fullscreen', True)    

    starting_win.mainloop()



def main_window():
    #Functions to play, stop and record audio in Python voice recorder
    #The recording is done as a thread to prevent it being the main process
    def start_recording(filename):
        #If recording is selected, then the thread is activated
        t1=threading.Thread(target=record_audio(filename))
        t1.start()
    
    def stop_recording():
        #To stop, set the flag to false
        global recording
        recording = False
        messagebox.showinfo(message="Recording finished")
    
    def play_recording(filename):
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
    def record_audio(filename): 
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
        os.remove(files_path)
        start_recording()

    def continue_func():
        sentence_file = sentences_folder[0]
        sentences_folder.remove(sentence_file)
        sentence_path = os.path.join(curr_dir, sentence_file)
        sentence = open(sentence_path).read()
        T.delete("1.0", "end")
        T.insert(tk.END, sentence)
        filename = sentence_file.replace('.txt', '.wav')
        voice_rec.update()

    curr_dir = '/Users/tomer/test'
    sentences_folder = os.listdir(curr_dir)
    for sen in sentences_folder:
        if not sen.endswith('.txt'):
            sentences_folder.remove(sen)

    try:
        curr_names_path = os.path.join(base_path, curr_name)
        curr_names_folder = os.mkdir(os.path.join(base_path, curr_name))
    except: # name already exists
        popup_win = Tk()
        
        


    #Define the user interface for Voice Recorder using Python
    voice_rec = Toplevel(starting_win)
    voice_rec.geometry("360x200")
    #Create a queue to contain the audio data
    q = queue.Queue()
    #Declare variables and initialise them
    recording = False
    file_exists = False

    #Progress Bar
    bar = Progressbar(voice_rec, length=400, style='black.Horizontal.TProgressbar')
    bar['value']=70
    
    #Text
    sentence_file = sentences_folder[0]
    sentences_folder.remove(sentence_file)
    sentence_path = os.path.join(curr_dir, sentence_file)
    sentence = open(sentence_path).read()
    #shutil.move(sentence_path, curr_names_path) # move the text file to the users folder
    T = Text()
    T.config(font=("Ariel", 20))
    T.insert(tk.END, sentence)
    global filename
    filename = sentence_file.replace('.txt', '.wav')
    global files_path
    files_path = os.path.join(base_path, filename)
    #shutil.move(files_path, curr_names_path)  # move the sound file to the users folder
    
    #Button to record audio
    record_btn = Button(voice_rec, width=20, text="Record Audio", command=start_recording)
    stop_btn = Button(voice_rec, width=20, text="Stop Recording", command=stop_recording)
    play_btn = Button(voice_rec, width=20, text="Play Recording", command=play_recording)
    record_again_btn = Button(voice_rec, command=record_again) 
    continue_btn = Button(voice_rec, text="Continue", command=continue_func)
    quit_btn = Button(voice_rec, text="Quit", command=voice_rec.destroy)
    
    record_btn.grid(row=1,column=0)
    stop_btn.grid(row=1,column=1)
    play_btn.grid(row=1,column=2)
    record_again_btn.grid(row=1, column=3)
    bar.grid(row=4, column=0, columnspan=2)
    T.grid(row=6, column=0, columnspan=3)
    continue_btn.grid(row=8, column=0)
    quit_btn.grid(row=8, column=1)
    voice_rec.attributes('-fullscreen', True)
    
    voice_rec.mainloop()



starting_window()
#main_window()