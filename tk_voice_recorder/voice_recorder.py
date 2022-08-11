#ProjectGurukul's Voice recorder
#Import necessary modules
from tkinter.filedialog import askdirectory
import sounddevice as sd
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import ttk
import tkinter as tk
import queue
import soundfile as sf
import threading
from tkinter import messagebox

#Functions to play, stop and record audio in Python voice recorder
#The recording is done as a thread to prevent it being the main process
def start_recording(filename):
    #If recording is selected, then the thread is activated
    t1=threading.Thread(target= record_audio)
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
    #delete the the last file and call record again
    pass

#Get the users name and folder path
starting_win = Tk()
t1= Text()
t1.insert(tk.END, "Enter your full name:")
e = Entry(starting_win, width=40)
t2 = Text()
t2.insert(tk.END, "Select folder")
folder_path = askdirectory()

#Loop through all the folders files


#Define the user interface for Voice Recorder using Python
voice_rec = Tk()
voice_rec.geometry("360x200")
voice_rec.title("ProjectGurukul's Voice Recorder")
#Create a queue to contain the audio data
q = queue.Queue()
#Declare variables and initialise them
recording = False
file_exists = False

#Label to display app title in Python Voice Recorder Project
title_lbl  = Label(voice_rec, text="ProjectGurukul's Voice Recorder").grid(row=0, column=0, columnspan=3)
 
#Progress Bar
bar = Progressbar(voice_rec, length=400, style='black.Horizontal.TProgressbar')
bar['value']=70
#Text
sentence = "displayed sentence"
T = Text()
T.config(font=("Ariel", 20))
T.insert(tk.END, sentence)
filename = "file"
#Button to record audio
record_btn = Button(voice_rec, width=20, text="Record Audio", command=start_recording(filename))
#Stop button
stop_btn = Button(voice_rec, width=20, text="Stop Recording", command=stop_recording())
#Play button
play_btn = Button(voice_rec, width=20, text="Play Recording", command=play_recording(filename))
#Record again
record_again_btn = Button(voice_rec, command=record_again()) 
#Position buttons
record_btn.grid(row=1,column=0)
stop_btn.grid(row=1,column=1)
play_btn.grid(row=1,column=2)
bar.grid(row=4, column=0, columnspan=2)
T.grid(row=6, column=0, columnspan=3)
voice_rec.attributes('-fullscreen', True)
voice_rec.mainloop()



