from tkinter import *
import tkinter as tk
import os

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
                    top1.destroy()
                    global users_path
                    users_path = os.path.join(base_path, user_name)

                    top2 = Toplevel()
                    label2 = tk.Label(top2, text="Great! so press continue on the button of the main page and continue recording the sentences")
                    exit_btn = tk.Button(top2, text="Exit", command=exit)
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

global base_path
base_path = '/Users/tomer/tk_voice_recorder'

win = Tk()

name_text = tk.Text(win, width=15, height=1, font=('Ariel', 14))
name_text.insert(tk.END, "Enter your full name:")

global e
e = tk.Entry(win)
e.focus_set()

okay_btn = tk.Button(win, text='Submit Name', command=getUserName)

name_text.grid(row=1, column=0)
e.grid(row=1, column=1)
okay_btn.grid(row=1, column=2)

win.mainloop()
