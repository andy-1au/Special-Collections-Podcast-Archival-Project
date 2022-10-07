import tkinter as tk #for GUI
from tkinter import filedialog, Text #pick the apps 
import os 
import requests
import xml.etree.ElementTree as XET
import pandas as pd 
import csv

#test message
#test again

root = tk.Tk() # holds the entire app

# Script for downloading podcasts(mp3) using rss feed(xml) tags, takes in the path to the rss feed
def downloadPodcast(path):
    print("Downloading Podcast")
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
            print(url + " has been downloaded") 
            open(filePath, 'wb').write(download.content) #writes the file to the path
    print("All podcasts has been downloaded")


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

def removePlaceholder(event):
    enterRSS.delete(0, "end")
    return None

def getRSSEntry(): 
    rssLink = enterRSS.get() # Get the RSS feed from the entry box
    print(rssLink) # DEBUG
    xmlPath = save_RSS_Feed() # Get the path to save the RSS feed, requires user input
    rssPath = downloadRSS(rssLink, xmlPath) # Get the path to the downloaded RSS feed
    downloadPodcast(rssPath) # Use the path of RSS feed for download podcast function

def downloadRSS(entry, xmlPath):
    response = requests.get(entry, allow_redirects=True)
    rssPath = os.path.join(xmlPath, "rss.xml")
    open(rssPath, 'wb').write(response.content) #writes the content of the rss feed to a specified file named podcast.xml
    print("RSS Feed has been downloaded")
    return rssPath # Return the path to the rss feed

#attach the canvas to the root
canvas = tk.Canvas(root, height=700, width=700, bg="#263D42") 
canvas.pack() #pack the canvas to the root so it can be seen

frame = tk.Frame(root, bg="white") #create a frame
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1) #place the frame in the middle of the canvas

# button for selecting the rss feed
chooseRSS = tk.Button(frame, text="Select RSS Feed", padx=10, pady=5, fg="white", bg="#263D42", command=select_RSS_Feed) 
chooseRSS.pack() 

# button for selecting the folder to save the podcasts
choosePodcastFolder = tk.Button(frame, text="Select Podcasts Folder", padx=10, pady=5, fg="white", bg="#263D42", command=podcast_Folder) 
choosePodcastFolder.pack() 

submitRSS = tk.Button(frame, text="Submit RSS Feed", padx=10, pady=5, fg="white", bg="#263D42", command=getRSSEntry)
submitRSS.pack()

# make an entry box for rss feed, add a float label in the entry box
enterRSS = tk.Entry(frame, width=50, borderwidth=5)
enterRSS.insert(0, "Enter RSS Feed")
enterRSS.bind("<Button-1>", removePlaceholder)
enterRSS.pack()

root.mainloop() #similar to html, this is what keeps the window open