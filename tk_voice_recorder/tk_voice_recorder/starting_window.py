import tkinter as tk
from tkinter import *
from tkinter import filedialog

def select_folder():
    folder_path = filedialog.askdirectory()
    return folder_path

starting_win = Tk()
starting_win.geometry("360x200")
t1= Text(height=1, width=25)
t1.insert(tk.END, "Enter your full name:")
e = tk.Entry(starting_win, width=30)
folder_path = Button(text="Browse", command=select_folder()).grid(row=2, column=0)
t1.grid(row=1, column=0)
e.grid(row=1, column=1)
#folder_path.grid(row=2, column=0)
name = e.get()
print(name)
print(folder_path)
starting_win.mainloop()

