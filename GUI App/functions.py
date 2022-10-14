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



class functions:
    
    def __init__(self, root, enterRSS, outputBox):
        self.root = root
        self.enterRSS = enterRSS
        self.outputBox = outputBox
        
    def openXML(xmlFile):
        tree = XET.parse(xmlFile)
        root = tree.getroot()
        return root

    def download_PD(self, path):
        self.printToGUI("Downloading Podcast\n")
        root = self.openXML(path) # call openXML() to get root of the xml file

        podcastFolderPath = self.podcast_Folder() # Get the path to save the podcast
        for child in root.findall('./channel/item/'): #finds all tags in xml file under the item tag
            tag = child.tag
            if tag == 'enclosure':
                url = child.attrib.get('url')
                if url.find('/'): #finds the last '/' in the url
                    fileName = url.rsplit('/', 1)[1] #gets the file name from the url
                    filePath = os.path.join(podcastFolderPath, fileName) #creates a path for the file to be saved
                download = requests.get(url, allow_redirects=True) #downloads the file
                self.printToGUI(url + " has been downloaded\n") 
                open(filePath, 'wb').write(download.content) #writes the file to the path
        self.printToGUI("All podcasts has been downloaded\n") 
        download.close() #closes the connection to the server
        self.printToGUI("Connection Closed\n") #DEBUG, even when the request is closed, the app window still runs

    #asks user to select a folder to save the podcasts
    #askdirectory() only lets user select a folder
    def podcast_Folder(self):
        podcastFolderPath = filedialog.askdirectory(initialdir="/", title="Select Where to Save the Podcasts")
        pdPathLabel = tk.Label(self.root, text="Save Podcasts Path: " + podcastFolderPath) # Create a label to display the path of the podcast folder
        pdPathLabel.pack()
        print(podcastFolderPath)
        return podcastFolderPath

    #asks user to select the RSS xml file and save the path 
    def select_RSS_Feed(self):
        xmlPath = filedialog.askopenfilename(initialdir="/", title="Select Your RSS File", filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
        # Create a label to display the path of the rss feed
        xmlPathLabel = tk.Label(self.root, text="RSS Feed Path: " + xmlPath)
        xmlPathLabel.pack()
        print(xmlPath)

    #asks user to select the folder to save the downloaded rss feed
    def save_RSS_Feed(self):
        xmlPath = filedialog.askdirectory(initialdir="/", title="Select Where to Save the RSS Feed")
        xmlPathLabel = tk.Label(self.root, text="Save RSS Feed Path: " + xmlPath)
        xmlPathLabel.pack() # Create a label to display the path of the rss feed
        print(xmlPath)
        return xmlPath

    # remove the default text from the entry box
    def remove_PH(self, event):
        self.enterRSS.delete(0, "end")
        return None

    # function to save the entered rss feed url to a string
    def get_RSS_Entry(self): 
        rssLink = self.enterRSS.get() # Get the RSS feed from the entry box
        print(rssLink) # DEBUG
        xmlPath = self.save_RSS_Feed() # Get the path to save the RSS feed, requires user input
        rssPath = self.downloadRSS(rssLink, xmlPath) # Get the path to the downloaded RSS feed
        self.download_PD(rssPath) # Use the path of RSS feed for download podcast function

    # function to download the rss feed from the url and return the path to the downloaded rss feed
    def downloadRSS(self, entry, xmlPath):
        response = requests.get(entry, allow_redirects=True)
        rssPath = os.path.join(xmlPath, "rss.xml")
        open(rssPath, 'wb').write(response.content) #writes the content of the rss feed to a specified file named podcast.xml
        self.printToGUI("RSS Feed has been downloaded\n")
        return rssPath 

    # make a function to print terminal output to the GUI textbox
    def printToGUI(self, text):
        print(text) # DEBUG     
        self.outputBox.insert("end", text + "")
        self.root.update()

