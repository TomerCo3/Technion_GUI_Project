import tkinter as tk
from tkinter import *
from tkinter import filedialog
 
def starting_window():
    starting_win = Tk()
    starting_win.geometry('400x200')

    def directory():
        # get a directory path by user
        global filepath
        filepath=filedialog.askdirectory(title="Dialog box")
        print(filepath)

    def getUserName():
        global user_name
        user_name = e.get()
        print(user_name)

    e = tk.Entry(starting_win)
    e.grid(row=1, column=0)
    e.focus_set()

    okay_btn = tk.Button(starting_win, text='Submit Name', command=getUserName)
    okay_btn.grid(row=1, column=1)
    dialog_btn = tk.Button(starting_win, text='Select Directory', command=directory)
    dialog_btn.grid(row=2, column=0)
    exit_btn = tk.Button(starting_win, text='Done', command=exit)
    exit_btn.grid(row=3, column=0)
    starting_win.attributes('-fullscreen', True)

    starting_win.mainloop()

starting_window()
