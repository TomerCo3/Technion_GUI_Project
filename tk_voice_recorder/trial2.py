from tkinter import *
import tkinter as tk

def continue_func():
    sentence = sentences_folder[0]
    sentences_folder.remove(sentence)
    t.delete("1.0", "end")
    t.insert(tk.END, sentence)
    gui_win.update()

sentences_folder = ["sentence 1", "sentence 2", "sentence 3"]

gui_win = Tk()
t = Text()
sentence = sentences_folder[0]
sentences_folder.remove(sentence)
t.insert(tk.END, sentence)

continue_btn = Button(gui_win, text="Continue", command=continue_func)

t.grid(row=1, column=0)
continue_btn.grid(row=2, column=0)

gui_win.mainloop()