import tkinter as tk
from tkinter import *
from tkinter import filedialog


starting_win = Tk()
starting_win.geometry('400x200')
starting_win.grid_rowconfigure(0, weight = 1)
starting_win.grid_columnconfigure(0, weight = 1)

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

def printstuff():
    print(user_name)
    print(filepath)

e = tk.Entry(starting_win)
e.grid(row=1, column=0)
e.focus_set()

curr_name = ''
curr_dir = ''

okay_btn = tk.Button(starting_win, text='Submit Name', command = lambda: curr_name==printText())
okay_btn.grid(row=1, column=1)
dialog_btn = tk.Button(starting_win, text='Select Directory', command = lambda: curr_dir==directory())
dialog_btn.grid(row=2, column=0)
exit_btn = tk.Button(starting_win, text='Done', command=exit)
exit_btn.grid(row=3, column=0)
#test_btn = tk.Button(starting_win, text='print', command=printstuff)
#test_btn.grid(row=4, column=0)

starting_win.mainloop()

