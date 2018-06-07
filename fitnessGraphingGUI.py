# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 14:36:09 2018

@author: pahlza
"""
import tkinter as tk
from tkinter import ttk
win = tk.Tk()
win.title('test#1')

ttk.Label(win, text='A Label').grid(column=0, row=0)

win.mainloop()