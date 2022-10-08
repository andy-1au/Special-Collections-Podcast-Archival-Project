import tkinter as tk #for GUI
from tkinter import filedialog, Text, CENTER
from tkinter import ttk
import os
from traceback import print_tb 
import requests
import xml.etree.ElementTree as XET
import pandas as pd 
import csv

# Script for downloading podcasts(mp3) using rss feed(xml) tags, takes in the path to the rss feed
def download_PD(path):
    printToGUI("Downloading Podcast\n")
    tree = XET.parse(path) #parse the xml file
    root = tree.getroot() #get the root of the xml file
    podcastFolderPath = podcast_Folder() # Get the path to save the podcast
    for child in root.findall('./channel/item/'): #finds all tags in xml file under the item tag
        tag = child.tag
        if tag == 'enclosure':
            url = child.attrib.get('url')
            if url.find('/'): #finds the last '/' in the url
                fileName = url.rsplit('/', 1)[1] #gets the file name from the url
                filePath = os.path.join(podcastFolderPath, fileName) #creates a path for the file to be saved
            download = requests.get(url, allow_redirects=True) #downloads the file
            printToGUI(url + " has been downloaded\n") 
            open(filePath, 'wb').write(download.content) #writes the file to the path
    printToGUI("All podcasts has been downloaded\n") 
    download.close() #closes the connection to the server
    printToGUI("Connection Closed\n") #DEBUG, even when the request is closed, the app window still runs

#asks user to select a folder to save the podcasts
#askdirectory() only lets user select a folder
def podcast_Folder():
    podcastFolderPath = filedialog.askdirectory(initialdir="/", title="Select Where to Save the Podcasts")
    pdPathLabel = tk.Label(root, text="Save Podcasts Path: " + podcastFolderPath) # Create a label to display the path of the podcast folder
    pdPathLabel.pack()
    print(podcastFolderPath)
    return podcastFolderPath

#asks user to select the RSS xml file and save the path 
def select_RSS_Feed():
    xmlPath = filedialog.askopenfilename(initialdir="/", title="Select Your RSS File", filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
    # Create a label to display the path of the rss feed
    xmlPathLabel = tk.Label(root, text="RSS Feed Path: " + xmlPath)
    xmlPathLabel.pack()
    print(xmlPath)

#asks user to select the folder to save the downloaded rss feed
def save_RSS_Feed():
    xmlPath = filedialog.askdirectory(initialdir="/", title="Select Where to Save the RSS Feed")
    xmlPathLabel = tk.Label(root, text="Save RSS Feed Path: " + xmlPath)
    xmlPathLabel.pack() # Create a label to display the path of the rss feed
    print(xmlPath)
    return xmlPath

# remove the default text from the entry box
def remove_PH(event):
    enterRSS.delete(0, "end")
    return None

# function to save the entered rss feed url to a string
def get_RSS_Entry(): 
    rssLink = enterRSS.get() # Get the RSS feed from the entry box
    print(rssLink) # DEBUG
    xmlPath = save_RSS_Feed() # Get the path to save the RSS feed, requires user input
    rssPath = downloadRSS(rssLink, xmlPath) # Get the path to the downloaded RSS feed
    download_PD(rssPath) # Use the path of RSS feed for download podcast function

# function to download the rss feed from the url and return the path to the downloaded rss feed
def downloadRSS(entry, xmlPath):
    response = requests.get(entry, allow_redirects=True)
    rssPath = os.path.join(xmlPath, "rss.xml")
    open(rssPath, 'wb').write(response.content) #writes the content of the rss feed to a specified file named podcast.xml
    printToGUI("RSS Feed has been downloaded\n")
    return rssPath 

# make a function to print terminal output to the GUI textbox
def printToGUI(text):
    print(text)
    outputBox.insert("end", text + "")
    root.update()

root = tk.Tk() # holds the entire app
root.title("Podcast Downloader")

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
canvas = tk.Canvas(root, height=1000, width=1000, bg="white").pack() #pack the canvas to the root so it can be seen

frame = tk.Frame(root, bg="black") #create a frame
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1) #place the frame in the root

# --------------  Buttons Section ----------------- 
#Select RSS Feed from File Button
tk.Button(frame, text="Select RSS Feed", padx=10, pady=5, fg="white", bg="#263D42", command=select_RSS_Feed).pack(side="top", fill="x") 

# Submit RSS Feed button
tk.Button(frame, text="Submit RSS Feed", padx=10, pady=5, fg="white", bg="#263D42", command=get_RSS_Entry).pack(side="top", fill="x")

# Quit button
tk.Button(frame, text="Quit", padx=10, pady=5, fg="white", bg="#263D42", command=root.destroy).pack(side="bottom", fill="x", expand=True)
# --------------  Buttons Section ----------------- 

# ----------------- Entry Section -----------------
# make an entry box for rss feed, add a float label in the entry box
enterRSS = tk.Entry(frame, width=50, borderwidth=5, bg="#263D42", fg="white")
enterRSS.configure(justify=CENTER)
enterRSS.insert("end", "Enter RSS Feed Here")
enterRSS.bind("<Button-1>", remove_PH)
enterRSS.pack(side="top", fill="x", expand=True)
# ----------------- Entry Section -----------------

# ----------------- Text Box Section -----------------
# make a text box for terminal output
outputBox = tk.Text(frame, height=50, width=50, borderwidth=5, bg="#263D42")
outputBox.pack()
# ----------------- Text Box Section -----------------

root.mainloop() #similar to html, this is what keeps the window open

