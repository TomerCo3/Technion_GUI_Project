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
        global sentences_folder
        sentences_folder = os.listdir(directory_path)
        for sen in sentences_folder:
            if not sen.endswith('.txt'): 
                sentences_folder.remove(sen)
        global sentence_file_name
        sentence_file_name = sentences_folder[0]
        global sentence
        sentences_folder.remove(sentence_file_name)
        try:
            sentence = open(os.path.join(directory_path, sentence_file_name)).read()
            global filename
            filename = sentence_file_name.replace('.txt', '.wav')
            path_displayed_text.delete("1.0", "end")
            path_displayed_text.insert(1.0, directory_path)
        except:
            path_displayed_text.delete("1.0", "end")
            path_displayed_text.insert(1.0, "Not a sentences directory, please choose other one")
        voice_rec.update()


def getUserName():
        global user_name
        user_name = e.get()
        global users_path
        users_path = os.path.join(base_path, user_name)
        if os.path.isdir(users_path) == False:
            users_path = os.path.join(base_path, user_name)
            curr_names_folder = os.mkdir(users_path)
        else: # directory already exists
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
                    label2.grid(row=1, column=0)
                    exit_btn.grid(row=2, column=0)

                top1 = Toplevel()
                label1 = tk.Label(top1, text="Name already in use, do you want to continue with the name given or enter a differant one?")
                continue_btn = tk.Button(top1, text="Continue", command=continue_with_name)
                newName_btn = tk.Button(top1, text="Enter a new name", command=enter_new_name)

                label1.grid(row=1, column=0, columnspan=2)
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
    base_path = '/Users/tomer/tk_voice_recorder' # specific to the computer 
    
    #Define the user interface for Voice Recorder using Python
    global voice_rec
    voice_rec = Tk()
    voice_rec.configure(bg='#4B4B4B')

    def continue_func():
        if T.get('1.0', 'end-1c') == "Hello, please type in your full name and choose the directory you will be working with, then press continue":
            sentence_file_name = sentences_folder[0]
            sentences_folder.remove(sentence_file_name)
            global sentence_path
            sentence_path = os.path.join(directory_path, sentence_file_name)
            sentence = open(sentence_path).read()
            T.delete("1.0", "end")
            T.insert(tk.END, sentence)
            T.tag_configure("center", justify='center')
            T.tag_add("center", 1.0, "end")
            T.tag_configure("highlight", background='black')
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
                    label.grid(row=1, column=0)
                    update_btn.grid(row=2, column=0)
                    remain_with_old_btn.grid(row=2, column=1)
                popup_window()

            sentence_file_name = sentences_folder[0]
            sentences_folder.remove(sentence_file_name)
            sentence_path = os.path.join(directory_path, sentence_file_name)
            sentence = open(sentence_path).read()
            T.delete("1.0", "end")
            T.insert(tk.END, sentence)
            T.tag_configure("center", justify='center')
            T.tag_add("center", 1.0, "end")
            T.tag_configure("highlight", background='black')
            filename = sentence_file_name.replace('.txt', '.wav')
            voice_rec.update()
           
    style = ttk.Style()
    style.theme_use('classic')

    global q
    #Create a queue to contain the audio data
    q = queue.Queue()
    #Declare variables and initialise them
    recording = False
    file_exists = False

    name_text = tk.Text(voice_rec, width=15, height=1, font=('Ariel', 14), bg='#4B4B4B', fg='light gray', highlightbackground='#4B4B4B')
    name_text.insert(tk.END, "Enter your full name:")
    directory_text = tk.Text(voice_rec, width=33, height=1, font=('Ariel', 14), bg='#4B4B4B', fg='light gray', highlightbackground='#4B4B4B')
    directory_text.insert(1.0, "Select the directory you will be working with:")
    # text to get the users name
    global e
    e = tk.Entry(voice_rec, bg='light gray', fg='#4B4B4B', highlightbackground='light gray')
    e.focus_set()

    okay_btn = tk.Button(voice_rec, text='Submit Name', bg='#4B4B4B', highlightbackground='#4B4B4B',  command=getUserName)
    dialog_btn = tk.Button(voice_rec, text='Select Directory', bg='#4B4B4B', highlightbackground='#4B4B4B', command=getDirectory)

    your_path_text = tk.Text(voice_rec, height=1, width=20, font=('Ariel', 14), bg='#4B4B4B', fg='light gray', highlightbackground='#4B4B4B')
    your_path_text.insert(1.0, "current working directory:")
    global path_displayed_text
    path_displayed_text = tk.Text(voice_rec, height=1, width=60, font=('Ariel', 14), bg='#4B4B4B', fg='light gray', highlightbackground='#4B4B4B')
    path_displayed_text.insert(1.0, "No directory has been chosen yet")
    text1 = tk.Text(voice_rec, height=1, width=100, font=('Ariel', 14), bg='#4B4B4B', fg='light gray', highlightbackground='#4B4B4B')
    text1.insert(1.0, "If you want to change your current directory, just press the 'Select Directory' again and choose a differant directory" )

    help_spacer1 = tk.Label(voice_rec, bg='#4B4B4B', text=" ")
    help_spacer2 = tk.Label(voice_rec, bg='#4B4B4B', text=" ")
    help_spacer3 = tk.Label(voice_rec, bg='#4B4B4B', text=" ")

    name_text.grid(row=1, column=0, sticky=tk.W)
    e.place(x=160, y=1)
    e.lift()
    okay_btn.place(x=375, y=0)
    help_spacer1.grid(row=2, column=0)
    directory_text.grid(row=3, column=0, sticky=tk.W)
    dialog_btn.place(x=300, y=44)
    help_spacer2.grid(row=4, column=0)
    your_path_text.grid(row=5, column=0, sticky=tk.W)
    path_displayed_text.place(x=185, y=95)
    help_spacer3.grid(row=6, column=0)
    text1.grid(row=7, column=0, columnspan=2, sticky=tk.W)

    # spacers to make space between top of the window to the buttom
    spacer1 = tk.Label(voice_rec, bg='#4B4B4B', text="")
    spacer2 = tk.Label(voice_rec, bg='#4B4B4B', fg='dark gray', text="---------------------------Recording Section----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    spacer3 = tk.Label(voice_rec, bg='#4B4B4B', text="")
    #grid the spacers
    spacer1.grid(row=8, column=0)
    spacer2.grid(row=9, column=0, columnspan=5, sticky=tk.W)
    spacer3.grid(row=10, column=0)

    #Progress Bar
    bar = Progressbar(voice_rec, length=1045, style='black.Horizontal.TProgressbar')
    bar['value']=70
    #Text
    sentence = "Hello, please type in your full name and choose the directory you will be working with, then press continue"
    global T
    T = Text(voice_rec, height=10, bg='light gray', fg='#4B4B4B', highlightbackground='#4B4B4B')
    T.config(font=("Ariel", 20))
    T.insert(tk.END, sentence)
    T.tag_configure("center", justify='center')
    T.tag_add("center", 1.0, "end")
    T.tag_configure("highlight", background='black')
    
    #Button to record audio
    record_btn = Button(voice_rec, text="Record Audio", bg='#4B4B4B', highlightbackground='#4B4B4B', command=start_recording)
    stop_btn = Button(voice_rec, text="Stop Recording", bg='#4B4B4B', highlightbackground='#4B4B4B', command=stop_recording)
    play_btn = Button(voice_rec, text="Play Recording", bg='#4B4B4B', highlightbackground='#4B4B4B', command=play_recording)
    record_again_btn = Button(voice_rec, text="Record Again", bg='#4B4B4B', highlightbackground='#4B4B4B', command=record_again) 
    continue_btn = Button(voice_rec, text="Continue", bg='#4B4B4B', highlightbackground='#4B4B4B', command=continue_func)
    quit_btn = Button(voice_rec, text="Quit", bg='#4B4B4B', highlightbackground='#4B4B4B', command=voice_rec.destroy)

    record_btn.place(x=0, y=250)
    stop_btn.place(x=120, y=250)
    play_btn.place(x=250, y=250)
    record_again_btn.place(x=380, y=250)
    bar.place(x=0, y=280)
    T.place(x=0, y=310)
    continue_btn.place(x=0, y=550)
    quit_btn.place(x=90, y=550)
    voice_rec.attributes('-fullscreen', True)
    voice_rec.mainloop()

main_window()