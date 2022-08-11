from tkinter import *
from tkinter import filedialog

gui_win = Tk()
gui_win.geometry('400x200')
gui_win.grid_rowconfigure(0, weight = 1)
gui_win.grid_columnconfigure(0, weight = 1)

def directory():
    # get a directory path by user
    global filepath
    filepath=filedialog.askdirectory(title="Dialog box")
    print(filepath)
    return filepath

def printText():
    user_name = e.get()
    print(user_name)
    return user_name

e = Entry(gui_win)
e.pack()
e.focus_set()

curr_name = ''
curr_dir = ''

okay_btn = Button(gui_win, text='okay', command = lambda: curr_name==printText())
okay_btn.pack()
dialog_btn = Button(gui_win, text='select directory', command = lambda: curr_dir==directory())
dialog_btn.pack()
exit_btn = Button(gui_win, text='Exit', command=exit)
exit_btn.pack()


gui_win.mainloop()
