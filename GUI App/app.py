from ctypes import sizeof
from functions import *
import tkinter as tk #for GUI
from tkinter import filedialog, Text, CENTER
from tkinter import ttk
from tkinter.messagebox import showerror
from threading import Thread
import requests
import os 
import xml.etree.ElementTree as XET
import pandas as pd 
import csv

root = tk.Tk() # holds the entire app
root.title("Podcast Downloader")
root.resizable(0, 0) # disable resizing the window

#------------------Working On Styling------------------
# #Add some styling to the app
# style = ttk.Style()
# style.configure("Treeview",
#     background = "silver",
#     foreground = "black",
#     rowheight = 25,
#     fieldbackground = "silver")

# style.map('Treeview',
#     background = [('selected', 'blue')]) 

# my_tree = ttk.Treeview(root)
#------------------Working On Styling------------------
#attach the canvas to the root
frame = tk.Frame(root, bg="black") #pack the canvas to the root so it can be seen
frame.pack()

# frame = tk.Frame(root, bg="black") #create a frame
# frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1) #place the frame in the root

# ----------------- Entry Section -----------------
# make an entry box for rss feed, add a float label in the entry box
enterRSS = tk.Entry(frame, width=20, borderwidth=5, bg="black", fg="white")
# ----------------- Entry Section -----------------

# ----------------- Text Box Section -----------------
# make a text box for terminal output
outputBox = tk.Text(frame, height=25, width=50, borderwidth=5, bg="black")
outputBox.pack(fill="both", expand=True)
# ----------------- Text Box Section -----------------
obj = functions(root, enterRSS, outputBox)

# --------------  Buttons Section ----------------- 
#Select RSS Feed from File Button
tk.Button(frame, text="Select RSS Feed", padx=10, pady=5, fg="white", bg="black", command=obj.select_RSS_Feed).pack(side="top", fill="both", expand=True)

# Submit RSS Feed butt
tk.Button(frame, text="Submit RSS Feed", padx=10, pady=5, fg="white", bg="black", command=obj.get_RSS_Entry).pack(side="top", fill="both", expand=True)

# Quit button
tk.Button(frame, text="Quit", padx=10, pady=5, fg="white", bg="black", command=root.destroy).pack(side="bottom", fill="both", expand=True)
# --------------  Buttons Section ----------------- 

enterRSS.configure(justify=CENTER)
enterRSS.insert("end", "Enter RSS Feed Here")
enterRSS.bind("<Button-1>", obj.remove_PH)
enterRSS.pack(side="top", fill="both", expand=True)

root.mainloop() #similar to html, this is what keeps the window open