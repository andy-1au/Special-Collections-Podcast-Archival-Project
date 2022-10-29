from pathlib import Path

import PySimpleGUI as sg 
import pandas as pd
import requests
import os 

#------------------RSS LINK------------------#
#https://feeds.captivate.fm/gogetters/
#------------------RSS LINK------------------#


# def convert_to_csv():
def download_RSS(url, rssDest):
    response = requests.get(url, allow_redirects=True)
    rssPath = os.path.join(rssDest, "rss.xml") #creates a path for the file to be saved
    open(rssPath, 'wb').write(response.content) #writes the content of the rss feed to a specified file named podcast.xml
    print("RSS Feed has been downloaded")
    return rssPath #not sure if this is needed

# def download_PD(xml, podcastDest): #look at app.py for reference 
    


#Layout
layout = [
        #each line in the layout list is a row 
        #LATER - add placeholder and disappear when clicked
        [sg.Text("RSS Feed Link:"), sg.Input(key="-RSS_URL-")],
        [sg.Text("XML File:"), sg.Input(key="-XML_File-"), sg.FileBrowse(file_types=(("XML Files", "*.xml"),))], 
        [sg.Text("RSS Destination:"), sg.Input(key="-RSS_DEST-"), sg.FolderBrowse()],
        [sg.Text("Podcast Destination:"), sg.Input(key="-POD_DEST-"), sg.FolderBrowse()],
        [sg.Text("CSV Destination:"), sg.Input(key="-CSV_DEST-"), sg.FolderBrowse()],
        [sg.Exit(), sg.Button("Download RSS"), sg.Button("Download Podcasts"), sg.Button("Convert To CSV")]    
]

window = sg.Window("Podcast Downloader", layout)

while True: 
    event, values = window.read() #get values and events from the GUI
    print(event, values) #DEBUG
    if event == sg.WIN_CLOSED or event == "Exit": #WIN_CLOSED = X button, Exit = Exit button
        break #break out of the loop and close the window
    if event == "Download RSS":
        print("Downloading RSS Feed") #DEBUG
        download_RSS(values["-RSS_URL-"], values["-RSS_DEST-"])
        
        
    if event == "Download Podcasts":
        print("Downloading Podcasts") #DEBUG 
    if event == "Convert To CSV":
        print("Converting To CSV") #DEBUG
window.close() 