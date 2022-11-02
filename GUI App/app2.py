# from ast import main
from pathlib import Path
# from pydoc import text
# from tkinter import Text
# from turtle import down

import PySimpleGUI as sg 
import pandas as pd
import xml.etree.ElementTree as XET
import csv
import requests
import os 


#------------------RSS LINK------------------#
#https://feeds.captivate.fm/gogetters/
#------------------RSS LINK------------------#

#NOTE: all we need to do is change the some itune tags in the xml file to simplier tags so that it can read easily
#NOTE: <link> tag is some kind of encoded link, we need to decode it (I think)
#NOTE: <enclosure> tag might not always be named the same
def convert_to_csv(wantedTags, xmlFile, csvDest):
    print("Converting to CSV file") #DEBUG
    root = open_XML(xmlFile)
    
    savePath = os.path.join(csvDest, "test.csv") #creates a path for the file to be saved
    
    podcast_CSV = open(savePath, 'w', newline='') #opens the file in write mode
    
    csv_writer = csv.writer(podcast_CSV)
    podcast_header = [] 
    for tag in wantedTags:
        podcast_header.append(tag) 
    csv_writer.writerow(podcast_header)

    # find the number of item tags used for the for loop later
    numItems = num_of_items(xmlFile)

    print("Number of item tags: " + str(numItems)) #DEBUG
    
    # loop through all the item tags, one at a time
    for i in range(numItems): #prevents index out of bound error for the root.findall() function
        podcast_row = [] #empty every time the loop runs
        for tag in wantedTags:
            for child in root.findall('./channel/item[' + str(i+1) + ']/'): #i+1 is the index of the item tag, the first item tag always starts at index 1
                if child.tag == 'enclosure' and tag == 'enclosure':
                    podcast_row.append(child.attrib.get('url'))
                elif child.tag == tag:
                    podcast_row.append(child.text)
        csv_writer.writerow(podcast_row)
    podcast_CSV.close()

def num_of_items(xmlFile):
    root = open_XML(xmlFile)
    numItems = 0
    for child in root.findall('./channel/'):
        if child.tag == 'item':
            numItems += 1
    return numItems

def get_tags(xmlFile):
    originalTags = []
    tagsList = []
       
    root = open_XML(xmlFile)
    for i in root.findall('./channel/item/'):
        tag = i.tag
        otag = i.tag
        if otag not in originalTags:
            originalTags.append(otag)
        # some tags have {} in them with contents, remove it and replace it with 'itunes'
        if tag.find('{') != -1:
            tag = tag.replace(tag[1:tag.find('}')], 'itunes')
        # add the tag to the list
        if tag not in tagsList:
            tagsList.append(tag)
            
    print(tagsList)
    print(originalTags)
    return tagsList

def download_RSS(url, rssDest):
    print("Downloading RSS Feed") #DEBUG
    response = requests.get(url, allow_redirects=True)
    rssPath = os.path.join(rssDest, "rss.xml") #creates a path for the file to be saved
    open(rssPath, 'wb').write(response.content) #writes the content of the rss feed to a specified file named podcast.xml
    print("RSS Feed has been downloaded")
    return rssPath #not sure if this is needed

# Keep in mind that this function causes the program to lag for a few seconds when the download happens
def download_PD(xmlFile, podcastDest): #look at app.py for reference 
    print("Downloading Podcast") #DEBUG
    root = open_XML(xmlFile) # call open_XML() to get root of the xml file
    
    for child in root.findall('./channel/item/'): #finds all tags in xml file under the item tag
        tag = child.tag
        if tag == 'enclosure':
            url = child.attrib.get('url')
            if url.find('/'): #finds the last '/' in the url
                fileName = url.rsplit('/', 1)[1] #split by '/' 1 time, get the second item in the list which is the mp3 file name
                filePath = os.path.join(podcastDest, fileName) #creates a path for the file to be saved
            download = requests.get(url, allow_redirects=True) #downloads the file
            print(fileName + " has been downloaded") #DEBUG
            open(filePath, 'wb').write(download.content) #writes the file to the path
    print("All podcasts have been downloaded") #DEBUG
    download.close() #closes the connection to the server
    print("Connection to server has been closed") #DEBUG

# Get root of xml file
def open_XML(xmlFile):
    tree = XET.parse(xmlFile)
    root = tree.getroot()
    return root

# Path validation    
def is_valid_path(filepath):
    if filepath and Path(filepath).exists(): #checks if the path is valid
        return True
    else:
        return False

def select_tags_windows(tagsList, xmlFile, csvDest):
    layout = [] #create empty layout and add to it later
    
    for tag in tagsList:
        layout.append([sg.Checkbox(tag, key=tag, default=False)])
    
    #add a column to the layout
    layout.append([sg.Column([[sg.Button("Cancel"), sg.Button("Save")]])])
    # layout.append([sg.Button("Cancel"), sg.Button("Save")])
    
    window = sg.Window("Select Tags", layout, modal=True)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            window.close()
            return None
        elif event == "Save":
            window.close()
            wantedTags = []
            if values:
                for tag in tagsList: 
                    if values[tag]: #checks if the tag is checked
                        wantedTags.append(tag)
            print(wantedTags) #DEBUG
            convert_to_csv(wantedTags, xmlFile, csvDest)
            

def settings_window():
    
    # dropdown list for theme
    layout = [
                [sg.Text("Font:"), sg.DropDown(values=sg.Text.fonts_installed_list(), default_value=settings["GUI"]["font_family"], key="-FONT-"), sg.Text("Font-Size:"), sg.Input(settings["GUI"]["font_size"], s=2, key="-F_SIZE-"), sg.Text("Theme:"), sg.DropDown(values=sg.theme_list(), default_value=settings["GUI"]["theme"], key="-THEME-")],
                [sg.Button("Cancel"), sg.Button("Save")]   
            ]
    
    window = sg.Window("Settings", layout, modal=True) #modal makes it so that user can't interact with the main window while the settings window is open
    
    while True:
        event, values = window.read()
        print(event, values) #DEBUG
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        if event == "Save":
            settings["GUI"]["font_family"] = values["-FONT-"]
            settings["GUI"]["font_size"] = values["-F_SIZE-"]
            settings["GUI"]["theme"] = values["-THEME-"]
            print(settings) #DEBUG
            
            sg.popup_no_titlebar("Settings have been saved")
            break
    window.close()
   
def main_window():
    
    # Menu Definition
    menu_def = [["Help", ["About", "Settings", "Exit"]]]
    
    # GUI Layout
    layout = [
        #each line in the layout list is a row separated by commas 
        #LATER - add placeholder and disappear when clicked
        [sg.MenubarCustom(menu_def, tearoff=False, key="-MENU-")],
        [sg.Text("RSS Feed Link:"), sg.Input(key="-RSS_URL-")],
        [sg.Text("XML File:"), sg.Input(key="-XML_File-"), sg.FileBrowse(file_types=(("XML Files", "*.xml"),))], 
        [sg.Text("RSS Destination:"), sg.Input(key="-RSS_DEST-"), sg.FolderBrowse()],
        [sg.Text("Podcast Destination:"), sg.Input(key="-POD_DEST-"), sg.FolderBrowse()],
        [sg.Text("CSV Destination:"), sg.Input(key="-CSV_DEST-"), sg.FolderBrowse()],
        [sg.Exit(), sg.Button("Settings"), sg.Button("Download RSS"), sg.Button("Download Podcasts"), sg.Button("Convert To CSV"), sg.Button("Open CSV")]  
    ]

    window_title = settings["GUI"]["title"]
    window = sg.Window(window_title, layout)

    # Keep reading the window's values, until an Exit event is found or the window is closed
    while True: 
        event, values = window.read() #get values and events from the GUI
        print(event, values) #DEBUG
        
        if event == sg.WIN_CLOSED or event == "Exit": #WIN_CLOSED = X button, Exit = Exit button
            break 
        
        if event == "About":
            window.disappear() #hide the main window
            sg.popup("Version: " + settings["About"]["version"], "Author: " + settings["About"]["author"], "Organization: " + settings["About"]["organization"], "Functionality: " + "Download RSS feeds & mp3 podcast files\n\t\t       Convert RSS to CSV format") #popup window
            window.reappear()
            
        if event == "Settings":
            settings_window()
        
        if event == "Download RSS":
            if (values["-RSS_URL-"] == ""):
                sg.popup("Please enter a RSS Feed Link")        
            elif not is_valid_path(values["-RSS_DEST-"]):
                sg.popup("Please enter a VALID file path for storing the RSS Feed")
            else:
                download_RSS(values["-RSS_URL-"], values["-RSS_DEST-"])
                
        if event == "Download Podcasts":
            if not is_valid_path(values["-XML_File-"]):
                sg.popup("Please enter a VALID file path for the location of the XML file")
            elif not is_valid_path(values["-POD_DEST-"]):
                sg.popup("Please enter a VALID file path for storing the podcasts")
            else:
                download_PD(values["-XML_File-"], values["-POD_DEST-"])
                
        if event == "Convert To CSV":
            if not is_valid_path(values["-XML_File-"]):
                sg.popup("Please enter a VALID file path for the location of the XML file")
            elif not is_valid_path(values["-CSV_DEST-"]):
                sg.popup("Please enter a VALID file path for storing the CSV file")
            else:
                list = get_tags(values["-XML_File-"])
                select_tags_windows(list, values["-XML_File-"], values["-CSV_DEST-"])
         
    window.close() 
    
if __name__ == "__main__":
    SETTINGS_PATH = Path.cwd() #gets the current working directory
    
    #Create the settings object and use ini format
    settings = sg.UserSettings(
        path=SETTINGS_PATH, filename="config.ini", use_config_file=True, convert_bools_and_none=True
    )
    theme = settings["GUI"]["theme"]
    font_family = settings["GUI"]["font_family"]
    font_size = settings["GUI"]["font_size"]
    sg.theme(theme)
    sg.set_options(font=(font_family, font_size))
    
    main_window() #call main_window() function after the settings have been loaded