from ctypes import sizeof
from re import T
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

#------------------RSS LINK------------------#
#https://feeds.captivate.fm/gogetters/
#------------------RSS LINK------------------#

# Script for downloading podcasts(mp3) using rss feed(xml) tags, takes in the path to the rss feed
def get_Tags():
    tagsList = []
    contentList = []

    xmlPath = filedialog.askopenfilename(initialdir="/", title="Select Your RSS File", filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
    root = open_XML(xmlPath)
    for i in root.findall('./channel/item/'):
        tag = i.tag
        # some tags have {} in them with contents, remove it and replace it with 'itunes'
        if tag.find('{') != -1:
            tag = tag.replace(tag[1:tag.find('}')], 'itunes')
        # add the tag to the list
        if tag not in tagsList:
            tagsList.append(tag)

    print(tagsList)
    return tagsList



def open_XML(xmlFile):
    tree = XET.parse(xmlFile)
    root = tree.getroot()
    return root
    
def download_PD(path):
    print_To_GUI("Downloading Podcast\n")
    root = open_XML(path) # call open_XML() to get root of the xml file

    podcastFolderPath = podcast_Folder() # Get the path to save the podcast
    for child in root.findall('./channel/item/'): #finds all tags in xml file under the item tag
        tag = child.tag
        if tag == 'enclosure':
            url = child.attrib.get('url')
            if url.find('/'): #finds the last '/' in the url
                fileName = url.rsplit('/', 1)[1] #gets the file name from the url
                filePath = os.path.join(podcastFolderPath, fileName) #creates a path for the file to be saved
            download = requests.get(url, allow_redirects=True) #downloads the file
            print_To_GUI(url + " has been downloaded\n") 
            open(filePath, 'wb').write(download.content) #writes the file to the path
    print_To_GUI("All podcasts have been downloaded\n") 
    download.close() #closes the connection to the server
    print_To_GUI("Connection Closed\n") #DEBUG, even when the request is closed, the app window still runs

#asks user to select a folder to save the podcasts
#askdirectory() only lets user select a folder
def podcast_Folder():
    podcastFolderPath = filedialog.askdirectory(initialdir="/", title="Select Where to Save the Podcasts")
    pdPathLabel = tk.Label(root, text="Save Podcasts Path: " + podcastFolderPath) # Create a label to display the path of the podcast folder
    pdPathLabel.pack()
    print(podcastFolderPath)
    return podcastFolderPath
 
#asks user to select the RSS xml file and save the path
#remove this later  
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
    rssPath = download_RSS(rssLink, xmlPath) # Get the path to the downloaded RSS feed
    download_PD(rssPath) # Use the path of RSS feed for download podcast function

# function to download the rss feed from the url and return the path to the downloaded rss feed
def download_RSS(entry, xmlPath):
    response = requests.get(entry, allow_redirects=True)
    rssPath = os.path.join(xmlPath, "rss.xml")
    open(rssPath, 'wb').write(response.content) #writes the content of the rss feed to a specified file named podcast.xml
    print_To_GUI("RSS Feed has been downloaded\n")
    return rssPath 

# make a function to print terminal output to the GUI textbox
def print_To_GUI(text):
    print(text) # DEBUG     
    outputBox.insert("end", text + "")
    root.update()

    

root = tk.Tk() # holds the entire app
#make the app open in a bigger window
root.geometry("800x600")
root.title("Podcast Downloader")
#root.resizable(0, 0) # disable resizing the window

# --------------  Buttons Section ----------------- 
#Select RSS Feed from File Button
#Create a section and style it just for the buttons, make it a frame on the left side of the window
buttonFrame = tk.Frame(root, bg="black")
buttonFrame.pack(side="left", fill="both", expand=False)

#Create a button to select the RSS feed from a file
selectRSSButton = tk.Button(buttonFrame, text="Select RSS Feed", command=select_RSS_Feed).pack()

#Create a button to submit the RSS feed url
submitRSSButton = tk.Button(buttonFrame, text="Submit RSS Feed", command=get_RSS_Entry).pack()

#Create a button to get the tags and text from the RSS feed
getTagsButton = tk.Button(buttonFrame, text="Get Tags", command=get_Tags).pack()


#Create a button to quit the app, put this button on the bottom of the button frame
quitButton = tk.Button(buttonFrame, text="Quit", command=root.quit).pack(side="bottom")

# --------------  Entry Section -----------------
#Create a section and style it just for the entry box, make it a frame on the right side of the window
entryFrame = tk.Frame(root, bg="black")
entryFrame.pack(side="right", fill="both", expand=False)

#Create an entry box for the RSS feed url
enterRSS = tk.Entry(entryFrame, width=50)
enterRSS.insert(0, "Enter RSS Feed URL")
enterRSS.bind("<Button-1>", remove_PH)
enterRSS.pack()

#put a terminal output box right below the entry box
outputBox = tk.Text(entryFrame, height=48, width=50).pack()

labelFrame = tk.Frame(root, bg="blue")
labelFrame.pack(side="top", fill="both", expand=True)




root.mainloop() #similar to html, this is what keeps the window open
